#!/usr/bin/env python3
"""
测试注册登录接口的脚本
功能：
1. 测试用户注册
2. 测试用户登录
3. 测试用户检查
4. 验证数据是否正确存储到数据库
"""

import requests
import json
import sqlite3
import os

# API 基础地址
BASE_URL = "http://localhost:5000/api"

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "auth.db")

def test_check_user(student_id):
    """测试检查用户是否存在接口"""
    print(f"\n=== 测试检查用户：{student_id} ===")
    url = f"{BASE_URL}/auth/check"
    data = {"student_id": student_id}
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result.get("data", {}).get("exists", False)
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_register(student_id, password):
    """测试用户注册接口"""
    print(f"\n=== 测试注册用户：{student_id} ===")
    url = f"{BASE_URL}/auth/register"
    data = {"student_id": student_id, "password": password}
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result.get("status") == "success"
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_login(student_id, password):
    """测试用户登录接口"""
    print(f"\n=== 测试登录用户：{student_id} ===")
    url = f"{BASE_URL}/auth/login"
    data = {"student_id": student_id, "password": password}
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result.get("status") == "success"
    except Exception as e:
        print(f"错误: {e}")
        return False

def check_database(student_id):
    """检查数据库中是否存在用户"""
    print(f"\n=== 检查数据库：{student_id} ===")
    
    try:
        # 连接数据库
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 查询用户
        cursor.execute('SELECT id, student_id, password, created_at FROM users WHERE student_id = ?', (student_id,))
        user = cursor.fetchone()
        
        if user:
            print(f"用户存在于数据库中：")
            print(f"  ID: {user[0]}")
            print(f"  学号: {user[1]}")
            print(f"  密码哈希: {user[2]}")
            print(f"  创建时间: {user[3]}")
            return True
        else:
            print("用户不存在于数据库中")
            return False
    except Exception as e:
        print(f"数据库查询错误: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def test_health_check():
    """测试健康检查接口"""
    print("\n=== 测试健康检查 ===")
    url = f"{BASE_URL}/health"
    
    try:
        response = requests.get(url)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result.get("status") == "ok"
    except Exception as e:
        print(f"错误: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试注册登录接口...")
    
    # 测试数据
    test_student_id = "12345678"
    test_password = "123456"
    
    # 1. 测试健康检查
    health_ok = test_health_check()
    if not health_ok:
        print("\n❌ 健康检查失败，服务可能未启动")
        return
    
    # 2. 检查用户是否存在
    user_exists = test_check_user(test_student_id)
    
    # 3. 根据检查结果执行注册或登录
    if not user_exists:
        # 注册新用户
        register_ok = test_register(test_student_id, test_password)
        if not register_ok:
            print("\n❌ 注册失败")
            return
    
    # 4. 登录用户
    login_ok = test_login(test_student_id, test_password)
    if not login_ok:
        print("\n❌ 登录失败")
        return
    
    # 5. 检查数据库
    db_ok = check_database(test_student_id)
    if not db_ok:
        print("\n❌ 数据库检查失败")
        return
    
    print("\n✅ 所有测试通过！")
    print("\n测试总结：")
    print(f"- 健康检查: {'✅ 通过' if health_ok else '❌ 失败'}")
    print(f"- 用户检查: {'✅ 通过' if user_exists or register_ok else '❌ 失败'}")
    print(f"- 注册: {'✅ 通过' if register_ok else '⚠️  未执行'}")
    print(f"- 登录: {'✅ 通过' if login_ok else '❌ 失败'}")
    print(f"- 数据库存储: {'✅ 通过' if db_ok else '❌ 失败'}")

if __name__ == "__main__":
    main()
