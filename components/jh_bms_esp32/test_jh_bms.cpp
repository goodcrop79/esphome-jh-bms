#include "jh_bms_esp32.h"
#include <iostream>
#include <cstdio>

// 使用命名空间
using namespace jh_bms_esp32;

// 简单的测试程序，用于验证JhBmsEsp32类的通知功能
int main() {
    // 创建JhBmsEsp32实例
    JhBmsEsp32 bms;
    
    // 打印配置信息
    bms.dump_config();
    
    std::cout << "\n=== 测试通知功能 ===\n";
    
    // 模拟连接事件
    std::cout << "\n1. 模拟连接事件...\n";
    bms.gattc_event_handler(0, 0, nullptr);  // 模拟连接事件
    
    // 模拟搜索完成事件
    std::cout << "\n2. 模拟服务搜索完成...\n";
    bms.gattc_event_handler(2, 0, nullptr);  // 模拟搜索完成事件
    
    // 模拟注册通知事件
    std::cout << "\n3. 模拟注册通知...\n";
    bms.gattc_event_handler(3, 0, nullptr);  // 模拟注册通知事件
    
    // 执行更新
    std::cout << "\n4. 执行更新...\n";
    bms.update();
    
    // 模拟通知事件（使用用户提供的真实数据）
    std::cout << "\n5. 模拟接收通知事件...\n";
    bms.gattc_event_handler(4, 0, nullptr);  // 模拟通知事件
    
    // 再次执行更新
    std::cout << "\n6. 再次执行更新...\n";
    bms.update();
    
    // 模拟断开连接事件
    std::cout << "\n7. 模拟断开连接事件...\n";
    bms.gattc_event_handler(1, 0, nullptr);  // 模拟断开连接事件
    
    std::cout << "\n=== 测试完成 ===\n";
    std::cout << "所有测试已执行完毕。在实际应用中，系统会自动接收BMS发送的通知数据。\n";
    
    return 0;
}