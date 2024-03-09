#include <iostream>
#include <limits.h>
#include <unistd.h>

int main() {
    // Declaration of a character sequence with the maximum length of a
    // host name on a system: 
    char hostname[HOST_NAME_MAX];
    
    // get the hostname with function from unistd.h:
    gethostname(hostname, HOST_NAME_MAX);

    std::cout << "The hostname of the machine is: " << hostname << std::endl;
}