<?php
// unzip.php - Automates extraction of deployment files
// Access this file via your browser: http://your-domain.com/unzip.php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

function unzip_file($zipFile) {
    if (!file_exists($zipFile)) {
        echo "<p style='color:red'>Error: $zipFile not found in the current directory.</p>";
        return false;
    }

    $zip = new ZipArchive;
    $res = $zip->open($zipFile);
    if ($res === TRUE) {
        $zip->extractTo('./');
        $zip->close();
        echo "<p style='color:green'>Success: $zipFile extracted successfully!</p>";
        return true;
    } else {
        echo "<p style='color:red'>Error: Could not open $zipFile. Error Code: $res</p>";
        return false;
    }
}

echo "<h1>Deployment Unzipper</h1>";
echo "<p>Starting extraction...</p>";

// 1. Extract Frontend
unzip_file('UPLOAD_THIS.zip');

// 2. Extract Backend (contains php-backend folder)
unzip_file('backend_deploy.zip');

echo "<hr>";
echo "<p><strong>Next Steps:</strong></p>";
echo "<ol>";
echo "<li>Go to <code>php-backend/db.php</code> in your File Manager and update database credentials.</li>";
echo "<li>Download <code>php-backend/portfolio_export.sql</code> (or find it in File Manager) and import it into your phpMyAdmin.</li>";
echo "<li>Delete this <code>unzip.php</code> file and the zip files when done.</li>";
echo "</ol>";
?>
