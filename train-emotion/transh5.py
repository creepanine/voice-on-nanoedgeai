import tensorflow as tf
import os

# 自定义 InputLayer 修复反序列化问题
class CustomInputLayer(tf.keras.layers.InputLayer):
    @classmethod
    def from_config(cls, config):
        if 'batch_shape' in config:
            config['batch_input_shape'] = config.pop('batch_shape')
        return super().from_config(config)

# 加载原始模型（需指定 custom_objects）
try:
    model = tf.keras.models.load_model(
        'saved_model/emotion_model.keras',  # 原始模型路径
        custom_objects={'InputLayer': CustomInputLayer}
    )
    print("模型加载成功")
except Exception as e:
    print(f"模型加载失败: {e}")
    exit()

# 显式重建 Sequential 模型架构（关键修改！）
def rebuild_sequential_model(original_model):
    # 获取输入形状（直接从模型的 input_shape 属性）
    input_shape = original_model.input_shape[1:]  # (48, 48, 1)
    
    # 重建 Sequential 模型
    new_model = tf.keras.Sequential(name="emotion_model_rebuilt")
    
    # 严格复制每一层的配置（包括参数）
    # ----------------------------------------------------------------
    # 第 0 层: Conv2D
    new_model.add(tf.keras.layers.Conv2D(
        filters=64,
        kernel_size=(3, 3),
        strides=(1, 1),  # 显式指定步幅
        padding='same',  # 关键！必须与原模型一致（推测原模型使用 'same' 填充）
        activation='relu',
        input_shape=input_shape,
        name='rebuilt_conv2d'
    ))
    
    # 第 1 层: BatchNormalization
    new_model.add(tf.keras.layers.BatchNormalization())
    
    # 第 2 层: Conv2D
    new_model.add(tf.keras.layers.Conv2D(
        filters=64,
        kernel_size=(3, 3),
        padding='same',  # 保持与原模型一致
        activation='relu'
    ))
    
    # 第 3 层: BatchNormalization
    new_model.add(tf.keras.layers.BatchNormalization())
    
    # 第 4 层: MaxPooling2D
    new_model.add(tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2),
        strides=(2, 2)  # 显式指定步幅
    ))
    
    # 继续按原模型结构严格复制后续层...
    # 第 5 层: Conv2D (128 filters)
    new_model.add(tf.keras.layers.Conv2D(
        filters=128,
        kernel_size=(3, 3),
        padding='same',
        activation='relu'
    ))
    
    # 第 6 层: BatchNormalization
    new_model.add(tf.keras.layers.BatchNormalization())
    
    # 第 7 层: Conv2D (128 filters)
    new_model.add(tf.keras.layers.Conv2D(
        filters=128,
        kernel_size=(3, 3),
        padding='same',
        activation='relu'
    ))
    
    # 第 8 层: BatchNormalization
    new_model.add(tf.keras.layers.BatchNormalization())
    
    # 第 9 层: MaxPooling2D
    new_model.add(tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2),
        strides=(2, 2)
    ))
    
    # 第 10 层: Conv2D (256 filters)
    new_model.add(tf.keras.layers.Conv2D(
        filters=256,
        kernel_size=(3, 3),
        padding='same',
        activation='relu'
    ))
    
    # 第 11 层: BatchNormalization
    new_model.add(tf.keras.layers.BatchNormalization())
    
    # 第 12 层: Conv2D (256 filters)
    new_model.add(tf.keras.layers.Conv2D(
        filters=256,
        kernel_size=(3, 3),
        padding='same',
        activation='relu'
    ))
    
    # 第 13 层: BatchNormalization
    new_model.add(tf.keras.layers.BatchNormalization())
    
    # 第 14 层: MaxPooling2D
    new_model.add(tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2),
        strides=(2, 2)
    ))
    
    # 第 15 层: Flatten
    new_model.add(tf.keras.layers.Flatten())
    
    # 第 16 层: Dense (128 units)
    new_model.add(tf.keras.layers.Dense(128, activation='relu'))
    
    # 第 17 层: BatchNormalization
    new_model.add(tf.keras.layers.BatchNormalization())
    
    # 第 18 层: Dense (7 units)
    new_model.add(tf.keras.layers.Dense(7, activation='softmax'))
    
    return new_model

# 重建模型并加载权重
new_model = rebuild_sequential_model(model)
new_model.set_weights(model.get_weights())

# 保存为 H5 格式
os.makedirs('saved_model', exist_ok=True)
new_model.save('saved_model/emotion_model.h5')
print("H5 模型保存成功")

# 验证新模型可重新加载
try:
    test_model = tf.keras.models.load_model('saved_model/emotion_model.h5')
    test_model.summary()
    print("H5 模型验证通过")
except Exception as e:
    print(f"H5 模型验证失败: {e}")