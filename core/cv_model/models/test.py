# https://stackoverflow.com/questions/58119155/freezing-graph-to-pb-in-tensorflow2

import tensorflow as tf
from tensorflow import keras
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2
import numpy as np

#set mobilenetv2 as a example
model = tf.saved_model.load("./mobilenet_model")
infer = model.signatures["serving_default"]

full_model = tf.function(lambda x:infer(x))
full_model = full_model.get_concrete_function(
    tf.TensorSpec(infer.inputs[0].shape, infer.inputs[0].dtype))

# Get frozen ConcreteFunction
frozen_func = convert_variables_to_constants_v2(full_model)
frozen_func.graph.as_graph_def()

layers = [op.name for op in frozen_func.graph.get_operations()]
print("-" * 50)
print("Frozen model layers: ")
for layer in layers:
    print(layer)

print("-" * 50)
print("Frozen model inputs: ")
print(frozen_func.inputs)
print("Frozen model outputs: ")
print(frozen_func.outputs)

# Save frozen graph from frozen ConcreteFunction to hard drive
tf.io.write_graph(graph_or_graph_def=frozen_func.graph, logdir=".", name="frozen_graph.pb", as_text=False)


def wrap_frozen_graph(graph_def, inputs, outputs, print_graph=False):
    def _imports_graph_def():
        tf.compat.v1.import_graph_def(graph_def, name="")

    wrapped_import = tf.compat.v1.wrap_function(_imports_graph_def, [])
    import_graph = wrapped_import.graph

    print("-" * 50)
    print("Frozen model layers: ")
    layers = [op.name for op in import_graph.get_operations()]
    if print_graph == True:
        for layer in layers:
            print(layer)
    print("-" * 50)

    return wrapped_import.prune(tf.nest.map_structure(import_graph.as_graph_element, inputs), tf.nest.map_structure(import_graph.as_graph_element, outputs))

## Example Usage ###
# Load frozen graph using TensorFlow 1.x functions
with tf.io.gfile.GFile("./frozen_graph.pb", "rb") as f:
    graph_def = tf.compat.v1.GraphDef()
    loaded = graph_def.ParseFromString(f.read())

# Wrap frozen graph to ConcreteFunctions
frozen_func = wrap_frozen_graph(graph_def=graph_def,
                                inputs=["x:0"],
                                outputs=["Identity:0","Identity_1:0","Identity_2:0",
                                "Identity_3:0","Identity_4:0","Identity_5:0",
                                "Identity_6:0","Identity_7:0"],
                                print_graph=False)
print("-" * 50)
print("Frozen model inputs: ")
print(frozen_func.inputs)
print("Frozen model outputs: ")
print(frozen_func.outputs)
# Get predictions for test images
rand_input = np.random.random((1, 50, 50, 3))*255
predictions = frozen_func(x=tf.constant(rand_input, dtype=tf.uint8))
# Print the prediction for the first image
print("-" * 50)
print("Example prediction reference:")
print(predictions[0].numpy())