#include "client.h"

#include <unistd.h>

Client::Client(int sock) : sock(sock) {}

Client::~Client()
{
	close(sock);
}
