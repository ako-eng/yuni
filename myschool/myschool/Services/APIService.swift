import Foundation

// MARK: - API Configuration
enum APIConfiguration {
    static let fixedPublicAPIRoot = "http://134.175.183.224:5000"
    
    static var baseURL: URL {
        URL(string: fixedPublicAPIRoot)! // 固定使用公网地址
    }
    
    static var baseURLString: String {
        fixedPublicAPIRoot
    }
    
    static func clearLegacyUserDefaults() {
        // 清理旧的 UserDefaults 配置
        UserDefaults.standard.removeObject(forKey: "myschool.api.baseURL")
    }
}

// MARK: - DTOs

// User Related
struct UserLoginRequest: Codable {
    let student_id: String
    let password: String
}

struct UserRegisterRequest: Codable {
    let student_id: String
    let password: String
    let name: String
    let department: String
    let major: String
    let grade: String
}

struct UserResponse: Codable {
    let status: String
    let message: String
    let data: UserData?
}

struct UserData: Codable {
    let id: Int
    let student_id: String
    let name: String
    let department: String
    let major: String
    let grade: String
}

struct UserInfoResponse: Codable {
    let status: String
    let data: UserInfoData?
}

struct UserInfoData: Codable {
    let id: Int
    let student_id: String
    let name: String
    let department: String
    let major: String
    let grade: String
    let avatar_name: String?
}

// Notice Related
struct NoticesPageResponse: Codable {
    let total: Int
    let page: Int
    let perPage: Int
    let pages: Int
    let items: [NoticeItemResponse]
}

struct NoticeItemResponse: Codable {
    let title: String
    let url: String
    let date: String
    let category: String
    let tags: [String]
    let content: String
    let publishDate: String?
    let department: String
    let attachments: [String]
    let sourceUrl: String
}

struct CategoriesResponse: Codable {
    let categories: [CategoryResponse]
    let total_notices: Int
    let all_tags: [String]
}

struct CategoryResponse: Codable {
    let name: String
    let count: Int
    let tags: [String]
}

// Course Related
struct CourseResponse: Codable {
    let status: String
    let data: [CourseData]?
}

struct CourseData: Codable {
    let id: String
    let name: String
    let teacher: String
    let room: String
    let day_of_week: Int
    let start_period: Int
    let end_period: Int
    let color_index: Int
    let weeks: String
}

struct CourseRequest: Codable {
    let id: String?
    let user_id: Int
    let name: String
    let teacher: String
    let room: String
    let day_of_week: Int
    let start_period: Int
    let end_period: Int
    let color_index: Int
    let weeks: String
}

// Grade Related
struct GradeResponse: Codable {
    let status: String
    let data: [GradeData]?
}

struct GradeData: Codable {
    let id: String
    let course_name: String
    let credit: Double
    let score: Int
    let grade_point: Double
    let semester: String
}

struct GradeRequest: Codable {
    let id: String?
    let user_id: Int
    let course_name: String
    let credit: Double
    let score: Int
    let grade_point: Double
    let semester: String
}

// Exam Related
struct ExamResponse: Codable {
    let status: String
    let data: [ExamData]?
}

struct ExamData: Codable {
    let id: String
    let course_name: String
    let exam_date: Double
    let location: String
    let seat_number: String
}

struct ExamRequest: Codable {
    let id: String?
    let user_id: Int
    let course_name: String
    let exam_date: Double
    let location: String
    let seat_number: String
}

// Award Related
struct AwardResponse: Codable {
    let status: String
    let data: [AwardData]?
}

struct AwardData: Codable {
    let id: String
    let name: String
    let level: String
    let date: Double
    let category: String
}

struct AwardRequest: Codable {
    let id: String?
    let user_id: Int
    let name: String
    let level: String
    let date: Double
    let category: String
}

// Search Related
struct SearchHistoryResponse: Codable {
    let status: String
    let data: [SearchHistoryData]?
}

struct SearchHistoryData: Codable {
    let keyword: String
    let search_time: Double
}

struct HotSearchResponse: Codable {
    let status: String
    let data: [HotSearchData]?
}

struct HotSearchData: Codable {
    let count: Int
    let keyword: String
}

struct SearchHistoryRequest: Codable {
    let user_id: Int
    let keyword: String
}

struct SearchHistoryDeleteRequest: Codable {
    let user_id: Int
    let keyword: String
}

// MARK: - API Service
actor APIService {
    static let shared = APIService()
    
    private let jsonDecoder = JSONDecoder()
    private let jsonEncoder = JSONEncoder()
    
    init() {
        jsonDecoder.keyDecodingStrategy = .convertFromSnakeCase
        jsonEncoder.keyEncodingStrategy = .convertToSnakeCase
    }
    
    // MARK: - Health Check
    func healthCheck() async throws -> Bool {
        guard let url = URL(string: "/api/health", relativeTo: APIConfiguration.baseURL)?.absoluteURL else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid URL"])
        }
        
        let (data, response) = try await URLSession.shared.data(from: url)
        
        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Health check failed"])
        }
        
        return true
    }
    
    // MARK: - Notice API
    func fetchNotices(page: Int, perPage: Int, baseURL: URL? = nil) async throws -> NoticesPageResponse {
        let root = rootOverride ?? APIConfiguration.baseURL
        var components = URLComponents(url: root.appendingPathComponent("api/notices"), resolvingAgainstBaseURL: true)!
        components.queryItems = [
            URLQueryItem(name: "page", value: String(page)),
            URLQueryItem(name: "per_page", value: String(perPage))
        ]
        
        let (data, response) = try await URLSession.shared.data(from: components.url!)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to fetch notices"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try jsonDecoder.decode(NoticesPageResponse.self, from: data)
    }
    
    func fetchCategories(baseURL: URL? = nil) async throws -> CategoriesResponse {
        let root = rootOverride ?? APIConfiguration.baseURL
        let url = root.appendingPathComponent("api/categories")
        
        let (data, response) = try await URLSession.shared.data(from: url)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to fetch categories"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try jsonDecoder.decode(CategoriesResponse.self, from: data)
    }
    
    func publishTeacherNotice(title: String, content: String, category: String, tags: [String], department: String) async throws {
        let requestData: [String: Any] = [
            "title": title,
            "content": content,
            "category": category,
            "tags": tags,
            "source": department
        ]
        
        var request = URLRequest(url: APIConfiguration.baseURL.appendingPathComponent("api/notices/add"))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONSerialization.data(withJSONObject: requestData)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to publish notice"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
    }
    
    // MARK: - User API
    func register(request: UserRegisterRequest) async throws -> UserResponse {
        let url = APIConfiguration.baseURL.appendingPathComponent("api/auth/register")
        var req = URLRequest(url: url)
        req.httpMethod = "POST"
        req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        req.httpBody = try jsonEncoder.encode(request)
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Registration failed"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try jsonDecoder.decode(UserResponse.self, from: data)
    }
    
    func login(request: UserLoginRequest) async throws -> UserResponse {
        let url = APIConfiguration.baseURL.appendingPathComponent("api/auth/login")
        var req = URLRequest(url: url)
        req.httpMethod = "POST"
        req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        req.httpBody = try jsonEncoder.encode(request)
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Login failed"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try jsonDecoder.decode(UserResponse.self, from: data)
    }
    
    func getUserInfo(user_id: Int) async throws -> UserInfoResponse {
        var components = URLComponents(url: APIConfiguration.baseURL.appendingPathComponent("api/user"), resolvingAgainstBaseURL: true)!
        components.queryItems = [URLQueryItem(name: "user_id", value: String(user_id))]
        
        let (data, response) = try await URLSession.shared.data(from: components.url!)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to get user info"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try jsonDecoder.decode(UserInfoResponse.self, from: data)
    }
    
    // MARK: - Course API
    func getCourses(user_id: Int) async throws -> CourseResponse {
        var components = URLComponents(url: APIConfiguration.baseURL.appendingPathComponent("api/courses"), resolvingAgainstBaseURL: true)!
        components.queryItems = [URLQueryItem(name: "user_id", value: String(user_id))]
        
        let (data, response) = try await URLSession.shared.data(from: components.url!)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to get courses"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try jsonDecoder.decode(CourseResponse.self, from: data)
    }
    
    func addCourse(request: CourseRequest) async throws -> [String: Any] {
        let url = APIConfiguration.baseURL.appendingPathComponent("api/courses")
        var req = URLRequest(url: url)
        req.httpMethod = "POST"
        req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        req.httpBody = try jsonEncoder.encode(request)
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to add course"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    func updateCourse(courseID: String, request: CourseRequest) async throws -> [String: Any] {
        let url = APIConfiguration.baseURL.appendingPathComponent("api/courses").appendingPathComponent(courseID)
        var req = URLRequest(url: url)
        req.httpMethod = "PUT"
        req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        req.httpBody = try jsonEncoder.encode(request)
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to update course"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    func deleteCourse(courseID: String, user_id: Int) async throws -> [String: Any] {
        var components = URLComponents(url: APIConfiguration.baseURL.appendingPathComponent("api/courses").appendingPathComponent(courseID), resolvingAgainstBaseURL: true)!
        components.queryItems = [URLQueryItem(name: "user_id", value: String(user_id))]
        
        var req = URLRequest(url: components.url!)
        req.httpMethod = "DELETE"
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to delete course"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    // MARK: - Grade API
    func getGrades(user_id: Int) async throws -> GradeResponse {
        var components = URLComponents(url: APIConfiguration.baseURL.appendingPathComponent("api/grades"), resolvingAgainstBaseURL: true)!
        components.queryItems = [URLQueryItem(name: "user_id", value: String(user_id))]
        
        let (data, response) = try await URLSession.shared.data(from: components.url!)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to get grades"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try jsonDecoder.decode(GradeResponse.self, from: data)
    }
    
    func addGrade(request: GradeRequest) async throws -> [String: Any] {
        let url = APIConfiguration.baseURL.appendingPathComponent("api/grades")
        var req = URLRequest(url: url)
        req.httpMethod = "POST"
        req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        req.httpBody = try jsonEncoder.encode(request)
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to add grade"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    func updateGrade(gradeID: String, request: GradeRequest) async throws -> [String: Any] {
        let url = APIConfiguration.baseURL.appendingPathComponent("api/grades").appendingPathComponent(gradeID)
        var req = URLRequest(url: url)
        req.httpMethod = "PUT"
        req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        req.httpBody = try jsonEncoder.encode(request)
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to update grade"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    func deleteGrade(gradeID: String, user_id: Int) async throws -> [String: Any] {
        var components = URLComponents(url: APIConfiguration.baseURL.appendingPathComponent("api/grades").appendingPathComponent(gradeID), resolvingAgainstBaseURL: true)!
        components.queryItems = [URLQueryItem(name: "user_id", value: String(user_id))]
        
        var req = URLRequest(url: components.url!)
        req.httpMethod = "DELETE"
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to delete grade"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    // MARK: - Exam API
    func getExams(user_id: Int) async throws -> ExamResponse {
        var components = URLComponents(url: APIConfiguration.baseURL.appendingPathComponent("api/exams"), resolvingAgainstBaseURL: true)!
        components.queryItems = [URLQueryItem(name: "user_id", value: String(user_id))]
        
        let (data, response) = try await URLSession.shared.data(from: components.url!)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to get exams"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try jsonDecoder.decode(ExamResponse.self, from: data)
    }
    
    func addExam(request: ExamRequest) async throws -> [String: Any] {
        let url = APIConfiguration.baseURL.appendingPathComponent("api/exams")
        var req = URLRequest(url: url)
        req.httpMethod = "POST"
        req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        req.httpBody = try jsonEncoder.encode(request)
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to add exam"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    func updateExam(examID: String, request: ExamRequest) async throws -> [String: Any] {
        let url = APIConfiguration.baseURL.appendingPathComponent("api/exams").appendingPathComponent(examID)
        var req = URLRequest(url: url)
        req.httpMethod = "PUT"
        req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        req.httpBody = try jsonEncoder.encode(request)
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to update exam"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    func deleteExam(examID: String, user_id: Int) async throws -> [String: Any] {
        var components = URLComponents(url: APIConfiguration.baseURL.appendingPathComponent("api/exams").appendingPathComponent(examID), resolvingAgainstBaseURL: true)!
        components.queryItems = [URLQueryItem(name: "user_id", value: String(user_id))]
        
        var req = URLRequest(url: components.url!)
        req.httpMethod = "DELETE"
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to delete exam"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    // MARK: - Award API
    func getAwards(user_id: Int) async throws -> AwardResponse {
        var components = URLComponents(url: APIConfiguration.baseURL.appendingPathComponent("api/awards"), resolvingAgainstBaseURL: true)!
        components.queryItems = [URLQueryItem(name: "user_id", value: String(user_id))]
        
        let (data, response) = try await URLSession.shared.data(from: components.url!)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to get awards"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try jsonDecoder.decode(AwardResponse.self, from: data)
    }
    
    func addAward(request: AwardRequest) async throws -> [String: Any] {
        let url = APIConfiguration.baseURL.appendingPathComponent("api/awards")
        var req = URLRequest(url: url)
        req.httpMethod = "POST"
        req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        req.httpBody = try jsonEncoder.encode(request)
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to add award"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    func updateAward(awardID: String, request: AwardRequest) async throws -> [String: Any] {
        let url = APIConfiguration.baseURL.appendingPathComponent("api/awards").appendingPathComponent(awardID)
        var req = URLRequest(url: url)
        req.httpMethod = "PUT"
        req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        req.httpBody = try jsonEncoder.encode(request)
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to update award"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    func deleteAward(awardID: String, user_id: Int) async throws -> [String: Any] {
        var components = URLComponents(url: APIConfiguration.baseURL.appendingPathComponent("api/awards").appendingPathComponent(awardID), resolvingAgainstBaseURL: true)!
        components.queryItems = [URLQueryItem(name: "user_id", value: String(user_id))]
        
        var req = URLRequest(url: components.url!)
        req.httpMethod = "DELETE"
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to delete award"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    // MARK: - Search API
    func getSearchHistory(user_id: Int) async throws -> SearchHistoryResponse {
        var components = URLComponents(url: APIConfiguration.baseURL.appendingPathComponent("api/search/history"), resolvingAgainstBaseURL: true)!
        components.queryItems = [URLQueryItem(name: "user_id", value: String(user_id))]
        
        let (data, response) = try await URLSession.shared.data(from: components.url!)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to get search history"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try jsonDecoder.decode(SearchHistoryResponse.self, from: data)
    }
    
    func addSearchHistory(request: SearchHistoryRequest) async throws -> [String: Any] {
        let url = APIConfiguration.baseURL.appendingPathComponent("api/search/history")
        var req = URLRequest(url: url)
        req.httpMethod = "POST"
        req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        req.httpBody = try jsonEncoder.encode(request)
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to add search history"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    func deleteSearchHistory(request: SearchHistoryDeleteRequest) async throws -> [String: Any] {
        let url = APIConfiguration.baseURL.appendingPathComponent("api/search/history")
        var req = URLRequest(url: url)
        req.httpMethod = "DELETE"
        req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        req.httpBody = try jsonEncoder.encode(request)
        
        let (data, response) = try await URLSession.shared.data(for: req)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to delete search history"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    func getHotSearches() async throws -> HotSearchResponse {
        var components = URLComponents(url: APIConfiguration.baseURL.appendingPathComponent("api/search/hot"), resolvingAgainstBaseURL: true)!
        
        let (data, response) = try await URLSession.shared.data(from: components.url!)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NSError(domain: "APIService", code: -1, userInfo: [NSLocalizedDescriptionKey: "Invalid response"])
        }
        
        if httpResponse.statusCode != 200 {
            let errorData = try? jsonDecoder.decode([String: String].self, from: data)
            let msg = errorData?["message"] ?? "Failed to get hot searches"
            throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: msg])
        }
        
        return try jsonDecoder.decode(HotSearchResponse.self, from: data)
    }
    
    // MARK: - Private
    private var rootOverride: URL? = nil
    
    private func setRootOverride(_ url: URL?) {
        rootOverride = url
    }
}