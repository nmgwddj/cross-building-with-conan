#include <iostream>
#include "json/json.h"

int main(int argc, char* argv[]) {
  Json::Value values;
  values["name"] = "John";
  values["age"] = 30;
  values["married"] = false;
  std::cout << values.toStyledString() << std::endl;
  return 0;
}
