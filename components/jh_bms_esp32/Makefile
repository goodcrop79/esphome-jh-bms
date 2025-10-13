# 编译工具
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -I.

# 目标文件
TARGET = test_jh_bms
OBJS = jh_bms_esp32.o test_jh_bms.o

# 编译规则
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

jh_bms_esp32.o: jh_bms_esp32.cpp jh_bms_esp32.h
	$(CXX) $(CXXFLAGS) -c -o $@ $<

test_jh_bms.o: test_jh_bms.cpp jh_bms_esp32.h
	$(CXX) $(CXXFLAGS) -c -o $@ $<

# 清理编译产物
clean:
	rm -f $(OBJS) $(TARGET)

# 运行测试
run: $(TARGET)
	./$(TARGET)

# 仅编译检查
check: $(OBJS)
	@echo "编译检查通过！"

.PHONY: all clean run check