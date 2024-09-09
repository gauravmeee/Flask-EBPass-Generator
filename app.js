const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const app = express();
const port = 3000;

// Set up multer for handling file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/')
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + path.extname(file.originalname))
  }
});
const upload = multer({ storage: storage });

// Serve static files
app.use(express.static('public'));
app.use('/uploads', express.static('uploads'));

// Parse URL-encoded bodies (as sent by HTML forms)
app.use(express.urlencoded({ extended: true }));

// Parse JSON bodies (as sent by API clients)
app.use(express.json());

// Route for the home page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Route for generating the bus pass
app.post('/generate-pass', upload.single('profilePic'), (req, res) => {
  const { name, validity, startDate, passNo } = req.body;
  const profilePicPath = req.file ? `/uploads/${req.file.filename}` : '';

  // In a real application, you'd probably save this data to a database
  const passData = {
    name,
    validity,
    startDate,
    passNo,
    profilePicPath
  };

  res.json(passData);
});

// Route for displaying the generated bus pass
app.get('/bus-pass', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'bus-pass.html'));
});

app.listen(port, () => {
  console.log(`e-Bus Pass generator app listening at http://localhost:${port}`);
});