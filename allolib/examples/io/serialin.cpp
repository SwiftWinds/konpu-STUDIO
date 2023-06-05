/***
 * This example expects the serial port has a loopback on it.
 *
 * Alternatively, you could use an Arduino:
 *
 * <pre>
 *  void setup() {
 *    Serial.begin(<insert your baudrate here>);
 *  }
 *
 *  void loop() {
 *    if (Serial.available()) {
 *      Serial.write(Serial.read());
 *    }
 *  }
 * </pre>
 */

/*
Here are the typical Arduino port addresses for each platform:
OSX		/dev/tty.usbmodem***
Linux	/dev/ttyACM0
MinGW	\\\\.\\COM3
*/

#include <cstdio>
#include <iostream>
#include <string>

#include "al/app/al_App.hpp"

// The serial library is included in the externals folder
#include "serial/serial.h"

using namespace std;

int run(string port, unsigned long baud) {
  // Argument 3 is the test string
  string test_string = "Testing.";

  // Create and open serial port with address and baudrate as arguments
  serial::Serial my_serial(port, baud, serial::Timeout::simpleTimeout(1000));

  cout << "Is the serial port open? "
       << (my_serial.isOpen() ? "Yes.\n" : "No.\n");

  // Wait a bit for serial device to setup
  al::wait(1);

  // Flush buffers
  my_serial.flush();

  // Test the timeout, there should be 1 second between prints
  cout << "Timeout == 1000ms, asking for 1 more byte than written." << endl;
  for (int count = 0; count < 10; ++count) {
    size_t bytes_wrote = my_serial.write(test_string);

    string result = my_serial.read(test_string.length() + 1);

    cout << "Iteration: " << count << ", Bytes written: " << bytes_wrote
         << ", Bytes read: " << result.length() << ", String read: " << result
         << endl;
  }

  // Test the timeout at 250ms
  my_serial.setTimeout(serial::Timeout::max(), 250, 0, 250, 0);
  cout << "Timeout == 250ms, asking for 1 more byte than written." << endl;
  for (int count = 0; count < 10; ++count) {
    size_t bytes_wrote = my_serial.write(test_string);

    string result = my_serial.read(test_string.length() + 1);

    cout << "Iteration: " << count << ", Bytes written: " << bytes_wrote
         << ", Bytes read: " << result.length() << ", String read: " << result
         << endl;
  }

  // Test the timeout at 250ms, but asking exactly for what was written
  cout << "Timeout == 250ms, asking for exactly what was written." << endl;
  for (int count = 0; count < 10; ++count) {
    size_t bytes_wrote = my_serial.write(test_string);

    string result = my_serial.read(test_string.length());

    cout << "Iteration: " << count << ", Bytes written: " << bytes_wrote
         << ", Bytes read: " << result.length() << ", String read: " << result
         << endl;
  }

  // Test the timeout at 250ms, but asking for 1 less than what was written
  cout << "Timeout == 250ms, asking for 1 less than was written." << endl;
  for (int count = 0; count < 10; ++count) {
    size_t bytes_wrote = my_serial.write(test_string);

    string result = my_serial.read(test_string.length() - 1);

    cout << "Iteration: " << count << ", Bytes written: " << bytes_wrote
         << ", Bytes read: " << result.length() << ", String read: " << result
         << endl;
  }

  return 0;
}

int main(int argc, char **argv) {
  string port("COM4");
  unsigned long baud = 115200;
  if (argc == 3) {
    port = argv[1];
    sscanf(argv[2], "%lu", &baud);
  }

  try {
    return run(port, baud);
  } catch (exception &e) {
    cerr << "Unhandled Exception: " << e.what() << endl;
  }
}
