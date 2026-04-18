import Foundation

struct MockData {
    static let notices: [Notice] = [
        Notice(
            id: "n001",
            title: "关于开展2024-2025学年第一学期选课的通知",
            summary: "2024-2025学年第一学期选课将于下周开始，请同学们及时关注选课系统，按时完成选课。",
            content: "2024-2025学年第一学期选课将于下周开始，请同学们及时关注选课系统，按时完成选课。具体选课时间和流程请查看教务系统通知。",
            category: .academic,
            source: "教务处",
            publishDate: Date().addingTimeInterval(-86400),
            isRead: false,
            isImportant: true,
            isUrgent: false,
            attachments: [],
            tags: ["选课", "教务"]
        ),
        Notice(
            id: "n002",
            title: "2024年全国大学生数学建模竞赛报名通知",
            summary: "2024年全国大学生数学建模竞赛报名工作已开始，请有意参加的同学及时报名。",
            content: "2024年全国大学生数学建模竞赛报名工作已开始，请有意参加的同学及时报名。报名截止时间为6月30日，详情请查看竞赛官网。",
            category: .competition,
            source: "学生处",
            publishDate: Date().addingTimeInterval(-172800),
            isRead: false,
            isImportant: true,
            isUrgent: false,
            attachments: [],
            tags: ["竞赛", "数学建模"]
        ),
        Notice(
            id: "n003",
            title: "校园网络安全知识讲座",
            summary: "为提高同学们的网络安全意识，信息中心将于本周五举办网络安全知识讲座。",
            content: "为提高同学们的网络安全意识，信息中心将于本周五举办网络安全知识讲座。讲座时间：本周五下午2:00，地点：图书馆报告厅。",
            category: .security,
            source: "信息中心",
            publishDate: Date().addingTimeInterval(-259200),
            isRead: true,
            isImportant: false,
            isUrgent: false,
            attachments: [],
            tags: ["安全", "讲座"]
        ),
        Notice(
            id: "n004",
            title: "关于2024届毕业生学位授予仪式的通知",
            summary: "2024届毕业生学位授予仪式将于6月20日举行，请相关同学做好准备。",
            content: "2024届毕业生学位授予仪式将于6月20日举行，请相关同学做好准备。具体时间和地点请查看学生处通知。",
            category: .academic,
            source: "学生处",
            publishDate: Date().addingTimeInterval(-345600),
            isRead: false,
            isImportant: true,
            isUrgent: false,
            attachments: [],
            tags: ["毕业", "学位"]
        ),
        Notice(
            id: "n005",
            title: "校园运动会报名通知",
            summary: "2024年校园运动会报名工作已开始，请同学们积极参与。",
            content: "2024年校园运动会报名工作已开始，请同学们积极参与。报名截止时间为5月30日，详情请查看体育教学部通知。",
            category: .life,
            source: "体育教学部",
            publishDate: Date().addingTimeInterval(-432000),
            isRead: true,
            isImportant: false,
            isUrgent: false,
            attachments: [],
            tags: ["体育", "运动会"]
        )
    ]
}
