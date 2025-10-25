<?php
// vul.php
// Vulnerable example: command injection and hardcoded secret

// --- VULN: Hardcoded secret ---
$API_KEY = "sk-proj-abc123def456ghi789jkl";

if (!empty($_GET['action']) && $_GET['action'] === 'lookup') {
    $host = isset($_GET['host']) ? $_GET['host'] : 'localhost'; // user-controlled

    // --- VULN: Command injection via shell execution ---
    // Dangerous: user input concatenated into shell command
    $output = shell_exec("ping -c 1 " . $host);
    echo "<pre>" . htmlspecialchars($output) . "</pre>";
}

// Simple endpoint demonstrating DB query vuln
if (!empty($_GET['user'])) {
    $user = $_GET['user'];
    // --- VULN: SQL Injection (if using mysql_query with string concat) ---
    // (Assuming old-style mysql_* usage for demonstration)
    // WARNING: mysql_* is deprecated; this is only to show a vulnerable pattern
    // $query = "SELECT * FROM users WHERE username = '$user'";
    // $res = mysql_query($query);
    // while ($row = mysql_fetch_assoc($res)) {
    //     echo htmlentities($row['username']);
    // }
    echo "Query for user: " . htmlentities($user);
}
?>