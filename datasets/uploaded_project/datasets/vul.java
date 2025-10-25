
// test_vul.java
// Vulnerable example: SQL injection and Runtime.exec with user input

import java.sql.*;
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class VulnerableServlet extends HttpServlet {
    private Connection getConnection() throws SQLException {
        // Example connection. Replace with your DB config in real tests.
        return DriverManager.getConnection("jdbc:sqlite::memory:");
    }

    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String user = req.getParameter("user"); // user-controlled

        // --- VULN: SQL Injection via string concatenation ---
        try (Connection conn = getConnection();
             Statement stmt = conn.createStatement()) {
            String query = "SELECT * FROM users WHERE username = '" + user + "'";
            ResultSet rs = stmt.executeQuery(query);
            while (rs.next()) {
                resp.getWriter().println("User: " + rs.getString("username"));
            }
        } catch (SQLException e) {
            resp.getWriter().println("DB error");
        }

        // --- VULN: Command injection via Runtime.exec with user input ---
        String host = req.getParameter("host"); // user-controlled
        try {
            // Dangerous: passes user input into shell command
            Process p = Runtime.getRuntime().exec("ping -c 1 " + host);
            BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String line;
            while ((line = br.readLine()) != null) {
                resp.getWriter().println(line);
            }
        } catch (Exception e) {
            resp.getWriter().println("Exec failed");
        }
    }
}
