// Sample Java class demonstrating hardcoded credentials and resource leak risks
import java.io.*;
import java.sql.*;

public class UserReportExporter {
    // Security: Hardcoded credential
    private static final String DB_PASS = "adminPass#2024!";

    public void exportData(String destinationPath, String filter) {
        try {
            Connection conn = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/production?user=root&password=" + DB_PASS
            );
            Statement stmt = conn.createStatement();
            
            // Security: SQL Injection
            ResultSet rs = stmt.executeQuery("SELECT * FROM reports WHERE category = '" + filter + "'");

            // Smell: Resource leak (FileInputStream/Writer not closed with try-with-resources)
            BufferedWriter writer = new BufferedWriter(new FileWriter(destinationPath));
            while (rs.next()) {
                writer.write(rs.getString("title"));
                writer.newLine();
            }
            // writer.close() is omitted on error path
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
