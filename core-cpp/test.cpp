#include <numeric>
#include "cppflow/include/Model.h"
#include "cppflow/include/Tensor.h"
#include <string>

#include <iomanip>


using namespace std;

int main(){
   Model model("/home/ravit/Konect-Code/spaspect-project/spaspect/core/cv_model/models/mobilenet-model/saved_model.pb");
   model.init();
   
   auto input_a = new Tensor(model, "input_a");
   auto input_b = new Tensor(model, "input_b");
   auto output  = new Tensor(model, "result");

   vector<float> data(100);
   iota(data.begin(), data.end(), 0);

   input_a->set_data(data);
   input_b->set_data(data);

   model.run({input_a, input_b}, output);
   for (float f : output->get_data<float>()) {
       cout << f << " ";
   }
   cout << endl;
   return 0;
}
