#include <numeric>
#include "cppflow/include/Model.h"
#include "cppflow/include/Tensor.h"
#include <string>

#include <iomanip>


using namespace std;


int main(){
   // loading and initializing the model
   Model model("../../core/cv_model/models/frozen_graph.pb");
   model.init();
   
   // setting up input and output tensors
   // Full mapping on here: https://docs.google.com/document/d/1caGy7Qj-p3SIrwQcepKB7ptHOgLLhPLslER5gKCbKAs/edit
   auto x = new Tensor(model, "x");
   auto detection_boxes = new Tensor(model, "Identity_1");
   auto detection_classes = new Tensor(model, "Identity_2");
   auto detection_scores = new Tensor(model, "Identity_4");
   auto num_detections = new Tensor(model, "Identity_5");

   // loading data into the vector
   vector<uint8_t> data(224*224*3);
   iota(data.begin(), data.end(), 0);


   for (int i = 0; i < 1000; ++i) {
      cout << "Running for iteration #" << to_string(i) << endl;

      // loading the data in the tensor
      x->set_data(data, {1, 224, 224, 3});

      // Passing the input tensors through the model
      model.run({x}, {num_detections, detection_boxes, detection_classes, detection_scores});

      /*
      vector<int64_t> detection_boxes_shape = detection_boxes->get_shape();
      string detection_boxes_shape_str = "";
      for (int i = 0; i < detection_boxes_shape.size(); ++i) {
         detection_boxes_shape_str += to_string(detection_boxes_shape[i]) + " ";
      }

      int num_detections_out = (int)num_detections->get_data<float>()[0];
      cout << "Number of detections is " << to_string(num_detections_out) << endl;

      cout << "Shape of output tensor is " << detection_boxes_shape_str << endl;*/
   }

   delete x;
   delete detection_boxes; //TODO: Add all other tensors

   return 0;
}
