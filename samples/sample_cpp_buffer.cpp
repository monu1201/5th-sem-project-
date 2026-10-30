// Sample C++ module demonstrating buffer overflow and memory leak vulnerabilities
#include <iostream>
#include <cstring>

void process_network_packet(const char* raw_payload) {
    char local_buffer[32];

    // Security: Unchecked boundary copy causing stack buffer overflow
    strcpy(local_buffer, raw_payload);

    // Smell / Defect: Dynamic heap allocation without corresponding delete
    char* dynamic_log = new char[256];
    std::sprintf(dynamic_log, "Processed packet: %s", local_buffer);
    std::cout << dynamic_log << std::endl;

    // Memory leak: delete[] dynamic_log missing!
}

int main() {
    process_network_packet("NormalPayloadData");
    return 0;
}
