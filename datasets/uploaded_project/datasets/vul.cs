// TestVul.cs
// Vulnerable example: SQL injection (string concat) and Process.Start with concatenated args

using System;
using System.Data.SqlClient;
using System.Diagnostics;
using System.Web;

public class TestVulHandler : IHttpHandler {
    public void ProcessRequest(HttpContext context) {
        var request = context.Request;
        var response = context.Response;

        string username = request.QueryString["username"]; // user-controlled
        string host = request.QueryString["host"]; // user-controlled

        // --- VULN: SQL Injection via string concatenation ---
        try {
            string connStr = "Server=(local);Database=Test;Trusted_Connection=True;";
            using (SqlConnection conn = new SqlConnection(connStr)) {
                conn.Open();
                string sql = "SELECT * FROM Users WHERE username = '" + username + "'";
                SqlCommand cmd = new SqlCommand(sql, conn);
                var reader = cmd.ExecuteReader();
                while (reader.Read()) {
                    response.Write("User: " + reader["username"]);
                }
            }
        } catch (Exception ex) {
            response.Write("DB error");
        }

        // --- VULN: Process.Start with concatenated args (command injection risk) ---
        try {
            // Dangerous: using user input directly in arguments can be abused
            ProcessStartInfo psi = new ProcessStartInfo("ping", "-n 1 " + host);
            psi.RedirectStandardOutput = true;
            psi.UseShellExecute = false;
            var process = Process.Start(psi);
            string output = process.StandardOutput.ReadToEnd();
            response.Write("<pre>" + HttpUtility.HtmlEncode(output) + "</pre>");
        } catch (Exception ex) {
            response.Write("Exec failed");
        }
    }

    public bool IsReusable { get { return false; } }
}