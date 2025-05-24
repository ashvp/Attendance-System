import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

class ApiService {
  static const String baseUrl = 'http://192.168.0.105:8000'; // Use your WSL IP

  // Multipart request for user registration with image upload
  static Future<http.StreamedResponse> registerUser({
    required String name,
    required String email,
    required File imageFile,
  }) async {
    final url = Uri.parse('$baseUrl/api/register');

    var request = http.MultipartRequest('POST', url);
    request.fields['name'] = name;
    request.fields['email'] = email;

    // Add the image file
    request.files.add(
      await http.MultipartFile.fromPath(
        'file',
        imageFile.path,
        contentType: MediaType('image', 'jpeg'), // adjust if your images differ
      ),
    );

    return await request.send();
  }

  // Example: other JSON-based APIs (if needed)
  static Future<http.StreamedResponse> markAttendance(String imagePath) async {
    final url = Uri.parse('$baseUrl/mark_attendance');
    var request = http.MultipartRequest('POST', url);
    request.files.add(
      await http.MultipartFile.fromPath('image', imagePath),
    );

    return await request.send();
  }

  static Future<http.Response> getAttendance(String userId) async {
    final url = Uri.parse('$baseUrl/attendance/user/$userId');
    return await http.get(url);
  }
}
