const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Initialize SQLite database
const db = new sqlite3.Database('./lotto.db', (err) => {
    if (err) {
        console.error('Error opening database:', err.message);
    } else {
        console.log('Connected to SQLite database');
        initDatabase();
    }
});

// Initialize database tables
function initDatabase() {
    db.serialize(() => {
        // Create lottery results table (539: 5 numbers from 1-39, no special number)
        db.run(`CREATE TABLE IF NOT EXISTS lottery_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            period TEXT NOT NULL UNIQUE,
            numbers TEXT NOT NULL,
            draw_date TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )`);

        // Create predictions table
        db.run(`CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            period TEXT NOT NULL,
            numbers TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )`);

        // Insert sample historical data if empty
        db.get("SELECT COUNT(*) as count FROM lottery_results", (err, row) => {
            if (row.count === 0) {
                insertSampleData();
            }
        });
    });
}

// Insert sample historical data from lotto539_data.json
function insertSampleData() {
    try {
        const jsonData = fs.readFileSync('./lotto539_data.json', 'utf8');
        const data = JSON.parse(jsonData);
        
        if (data.draws && Array.isArray(data.draws)) {
            const stmt = db.prepare("INSERT INTO lottery_results (period, numbers, draw_date) VALUES (?, ?, ?)");
            
            data.draws.forEach(draw => {
                // Calculate period number from date (民國年+月日)
                const dateParts = draw.date.split('-');
                const year = parseInt(dateParts[0]) - 1911;
                const month = dateParts[1].padStart(2, '0');
                const day = dateParts[2].padStart(2, '0');
                const periodNum = String(year) + month + day;
                
                // Format numbers with zero padding
                const numbersStr = draw.numbers.map(n => String(n).padStart(2, '0')).join(',');
                
                // Normalize date format to YYYY-MM-DD
                const normalizedDate = `${dateParts[0]}-${dateParts[1].padStart(2, '0')}-${dateParts[2].padStart(2, '0')}`;
                
                stmt.run(periodNum, numbersStr, normalizedDate);
            });
            
            stmt.finalize();
            console.log('Sample data inserted: ' + data.draws.length + ' records from lotto539_data.json');
        }
    } catch (err) {
        console.error('Error loading lotto539_data.json:', err.message);
    }
}

// ============ API Routes ============

// Get all lottery results
app.get('/api/results', (req, res) => {
    db.all("SELECT * FROM lottery_results ORDER BY draw_date DESC LIMIT 100", [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json({ success: true, data: rows });
    });
});

// Get latest result
app.get('/api/results/latest', (req, res) => {
    db.get("SELECT * FROM lottery_results ORDER BY id DESC LIMIT 1", [], (err, row) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json({ success: true, data: row });
    });
});

// Add new lottery result
app.post('/api/results', (req, res) => {
    const { period, numbers, draw_date } = req.body;
    
    if (!period || !numbers || !draw_date) {
        res.status(400).json({ success: false, message: '缺少必要參數' });
        return;
    }

    const stmt = db.prepare("INSERT INTO lottery_results (period, numbers, draw_date) VALUES (?, ?, ?)");
    stmt.run(period, numbers, draw_date, function(err) {
        if (err) {
            res.status(500).json({ success: false, message: err.message });
            return;
        }
        res.json({ success: true, message: '開獎結果已新增', id: this.lastID });
    });
    stmt.finalize();
});

// Get prediction for next period
app.get('/api/prediction', (req, res) => {
    // Get historical numbers for analysis (last 30 draws)
    db.all("SELECT numbers FROM lottery_results ORDER BY id DESC LIMIT 30", [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }

        // Analyze frequency
        const frequency = {};
        rows.forEach(row => {
            const nums = row.numbers.split(',').map(n => parseInt(n.trim()));
            nums.forEach(num => {
                frequency[num] = (frequency[num] || 0) + 1;
            });
        });

        // Sort by frequency and get top numbers
        const sorted = Object.entries(frequency)
            .sort((a, b) => b[1] - a[1])
            .map(([num]) => parseInt(num));

        // Generate prediction using weighted random
        const prediction = generatePrediction(sorted, frequency);
        
        res.json({ 
            success: true, 
            data: {
                numbers: prediction.numbers,
                analysis: {
                    hot_numbers: sorted.slice(0, 10),
                    frequency: frequency
                }
            }
        });
    });
});

// Generate prediction based on analysis
function generatePrediction(hotNumbers, frequency) {
    const selected = new Set();
    
    // Select some hot numbers
    const hotCount = Math.floor(Math.random() * 3) + 2; // 2-4 hot numbers
    
    while (selected.size < 5) {
        if (selected.size < hotCount && hotNumbers.length > 0) {
            const idx = Math.floor(Math.random() * Math.min(10, hotNumbers.length));
            selected.add(hotNumbers[idx]);
        } else {
            const num = Math.floor(Math.random() * 39) + 1;
            selected.add(num);
        }
    }

    const result = Array.from(selected).sort((a, b) => a - b);
    return {
        numbers: result.join(', ')
    };
}

// Save prediction
app.post('/api/prediction', (req, res) => {
    const { period, numbers } = req.body;
    
    if (!period || !numbers) {
        res.status(400).json({ success: false, message: '缺少必要參數' });
        return;
    }

    const stmt = db.prepare("INSERT INTO predictions (period, numbers) VALUES (?, ?)");
    stmt.run(period, numbers, function(err) {
        if (err) {
            res.status(500).json({ success: false, message: err.message });
            return;
        }
        res.json({ success: true, message: '預測已儲存', id: this.lastID });
    });
    stmt.finalize();
});

// Get number statistics (last 30 draws)
app.get('/api/statistics', (req, res) => {
    db.all("SELECT numbers FROM lottery_results ORDER BY id DESC LIMIT 30", [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }

        const frequency = {};
        const oddEven = { odd: 0, even: 0 };
        const ranges = { '1-10': 0, '11-20': 0, '21-30': 0, '31-39': 0 };

        rows.forEach(row => {
            const nums = row.numbers.split(',').map(n => parseInt(n.trim()));
            nums.forEach(num => {
                frequency[num] = (frequency[num] || 0) + 1;
                
                // Odd/Even
                if (num % 2 === 0) oddEven.even++;
                else oddEven.odd++;

                // Range
                if (num <= 10) ranges['1-10']++;
                else if (num <= 20) ranges['11-20']++;
                else if (num <= 30) ranges['21-30']++;
                else ranges['31-39']++;
            });
        });

        res.json({
            success: true,
            data: {
                frequency: frequency,
                oddEven: oddEven,
                ranges: ranges
            }
        });
    });
});

// Serve frontend
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
