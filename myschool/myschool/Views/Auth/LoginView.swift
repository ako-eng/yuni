import SwiftUI

struct LoginView: View {
    var onLoginSuccess: () -> Void

    @State private var studentId = ""
    @State private var password = ""
    @State private var agreedToTerms = false
    @State private var isVerifying = false
    @State private var errorMessage = ""

    private var studentIdValid: Bool {
        studentId.count >= 8
    }

    private var passwordValid: Bool {
        password.count >= 6
    }

    private var canLogin: Bool {
        agreedToTerms && studentIdValid && passwordValid
    }

    var body: some View {
        ScrollView {
            VStack(spacing: 0) {
                headerSection
                formSection
                Spacer(minLength: 40)
            }
        }
        .background(AppColors.background)
        .ignoresSafeArea(.container, edges: .top)
    }

    private var headerSection: some View {
        ZStack {
            LinearGradient(
                colors: [
                    Color(hex: 0x4A3F5C),
                    Color(hex: 0x6B5B7F),
                    Color(hex: 0x9B86B8),
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )

            VStack(spacing: 12) {
                Spacer().frame(height: 60)

                Image(systemName: "cup.and.saucer.fill")
                    .font(.system(size: 52))
                    .foregroundStyle(Color(hex: 0xFFF8F5))
                    .shadow(color: Color(hex: 0x4A3A5C).opacity(0.3), radius: 8, y: 4)

                Text("欢迎使用\(AppBranding.displayName)")
                    .font(.system(size: 22, weight: .bold, design: .rounded))
                    .foregroundStyle(.white)

                Text("软糯校园 · 一口掌握")
                    .font(.system(size: 14, weight: .medium, design: .rounded))
                    .foregroundStyle(.white.opacity(0.82))

                Spacer().frame(height: 30)
            }
        }
        .frame(height: 260)
        .clipShape(
            UnevenRoundedRectangle(
                bottomLeadingRadius: 28,
                bottomTrailingRadius: 28
            )
        )
    }

    private var formSection: some View {
        VStack(spacing: 16) {
            Text("未注册的学号验证后将自动创建账户")
                .font(.system(size: 12, weight: .medium, design: .rounded))
                .foregroundStyle(AppColors.textSecondary)
                .padding(.bottom, 4)

            if !errorMessage.isEmpty {
                Text(errorMessage)
                    .font(.system(size: 12, design: .rounded))
                    .foregroundStyle(.red)
                    .padding(.bottom, 4)
            }

            VStack(alignment: .leading, spacing: 8) {
                Text("学号")
                    .font(.system(size: 14, weight: .medium, design: .rounded))
                    .foregroundStyle(AppColors.textPrimary)

                HStack {
                    Image(systemName: "person.fill")
                        .foregroundStyle(AppColors.textSecondary)
                    TextField("请输入学号", text: $studentId)
                        .keyboardType(.numberPad)
                        .font(.system(size: 15, design: .rounded))
                }
                .padding(14)
                .background(AppColors.cardWhite)
                .clipShape(RoundedRectangle(cornerRadius: 12))
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(studentIdValid ? Color(hex: 0x9B86B8).opacity(0.4) : Color.gray.opacity(0.15), lineWidth: 1)
                )
            }

            VStack(alignment: .leading, spacing: 8) {
                Text("密码")
                    .font(.system(size: 14, weight: .medium, design: .rounded))
                    .foregroundStyle(AppColors.textPrimary)

                HStack {
                    Image(systemName: "lock.fill")
                        .foregroundStyle(AppColors.textSecondary)
                    SecureField("请输入密码", text: $password)
                        .font(.system(size: 15, design: .rounded))
                }
                .padding(14)
                .background(AppColors.cardWhite)
                .clipShape(RoundedRectangle(cornerRadius: 12))
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(passwordValid ? Color(hex: 0x9B86B8).opacity(0.4) : Color.gray.opacity(0.15), lineWidth: 1)
                )
            }

            HStack(spacing: 6) {
                Button {
                    withAnimation(AppleSpring.snappy) {
                        agreedToTerms.toggle()
                    }
                } label: {
                    Image(systemName: agreedToTerms ? "checkmark.circle.fill" : "circle")
                        .foregroundStyle(agreedToTerms ? Color(hex: 0x9B86B8) : AppColors.textSecondary)
                }
                Text("已阅读并同意")
                    .font(.system(size: 12, design: .rounded))
                    .foregroundStyle(AppColors.textSecondary)
                Text("《用户协议》")
                    .font(.system(size: 12, design: .rounded))
                    .foregroundStyle(Color(hex: 0x9B86B8))
                Text("和")
                    .font(.system(size: 12, design: .rounded))
                    .foregroundStyle(AppColors.textSecondary)
                Text("《隐私政策》")
                    .font(.system(size: 12, design: .rounded))
                    .foregroundStyle(Color(hex: 0x9B86B8))
            }
            .padding(.top, 4)

            Button {
                performLogin()
            } label: {
                HStack(spacing: 8) {
                    if isVerifying {
                        ProgressView()
                            .tint(.white)
                            .scaleEffect(0.8)
                    }
                    Text("登录 / 注册")
                        .font(.system(size: 17, weight: .semibold, design: .rounded))
                }
                .foregroundStyle(canLogin ? Color(hex: 0x4A3F5C) : .white.opacity(0.5))
                .frame(maxWidth: .infinity)
                .padding(.vertical, 16)
                .background(
                    Capsule()
                        .fill(canLogin ? Color.white : Color.white.opacity(0.15))
                        .shadow(color: Color(hex: 0x4A3F5C).opacity(canLogin ? 0.12 : 0), radius: 8, y: 4)
                )
                .overlay(
                    Capsule()
                        .stroke(canLogin ? Color(hex: 0x9B86B8).opacity(0.3) : Color.clear, lineWidth: 1)
                )
            }
            .disabled(!canLogin || isVerifying)
            .padding(.top, 8)

            Button {
            } label: {
                Text("忘记密码？")
                    .font(.system(size: 13, design: .rounded))
                    .foregroundStyle(AppColors.textSecondary)
            }
            .padding(.top, 4)
        }
        .padding(.horizontal, 24)
        .padding(.top, 28)
    }

    private func performLogin() {
        isVerifying = true
        errorMessage = ""
        UIImpactFeedbackGenerator(style: .medium).impactOccurred()

        // 检查用户是否存在
        checkUserExists {
            exists in
            if exists {
                // 用户存在，执行登录
                self.login()
            } else {
                // 用户不存在，执行注册
                self.register()
            }
        }
    }

    private func checkUserExists(completion: @escaping (Bool) -> Void) {
        guard let url = URL(string: "http://134.175.183.224:5000/api/auth/check") else {
            self.errorMessage = "网络错误"
            self.isVerifying = false
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body: [String: String] = ["student_id": studentId]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)

        URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    self.errorMessage = "网络错误: \(error.localizedDescription)"
                    self.isVerifying = false
                    return
                }

                guard let data = data else {
                    self.errorMessage = "网络错误"
                    self.isVerifying = false
                    return
                }

                do {
                    if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] {
                        if json["status"] as? String == "success",
                           let data = json["data"] as? [String: Any],
                           let exists = data["exists"] as? Bool {
                            completion(exists)
                        } else {
                            self.errorMessage = "服务器错误"
                            self.isVerifying = false
                        }
                    }
                } catch {
                    self.errorMessage = "解析错误"
                    self.isVerifying = false
                }
            }
        }.resume()
    }

    private func login() {
        guard let url = URL(string: "http://134.175.183.224:5000/api/auth/login") else {
            self.errorMessage = "网络错误"
            self.isVerifying = false
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body: [String: String] = ["student_id": studentId, "password": password]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)

        URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                self.isVerifying = false
                if let error = error {
                    self.errorMessage = "网络错误: \(error.localizedDescription)"
                    return
                }

                guard let data = data else {
                    self.errorMessage = "网络错误"
                    return
                }

                do {
                    if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] {
                        if json["status"] as? String == "success" {
                            // 登录成功
                            self.onLoginSuccess()
                        } else if let message = json["message"] as? String {
                            self.errorMessage = message
                        } else {
                            self.errorMessage = "登录失败"
                        }
                    }
                } catch {
                    self.errorMessage = "解析错误"
                }
            }
        }.resume()
    }

    private func register() {
        guard let url = URL(string: "http://134.175.183.224:5000/api/auth/register") else {
            self.errorMessage = "网络错误"
            self.isVerifying = false
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body: [String: String] = ["student_id": studentId, "password": password]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)

        URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                self.isVerifying = false
                if let error = error {
                    self.errorMessage = "网络错误: \(error.localizedDescription)"
                    return
                }

                guard let data = data else {
                    self.errorMessage = "网络错误"
                    return
                }

                do {
                    if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] {
                        if json["status"] as? String == "success" {
                            // 注册成功
                            self.onLoginSuccess()
                        } else if let message = json["message"] as? String {
                            self.errorMessage = message
                        } else {
                            self.errorMessage = "注册失败"
                        }
                    }
                } catch {
                    self.errorMessage = "解析错误"
                }
            }
        }.resume()
    }
}
