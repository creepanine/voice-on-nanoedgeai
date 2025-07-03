
/**
  ******************************************************************************
  * @file    app_x-cube-ai.c
  * @author  X-CUBE-AI C code generator
  * @brief   AI program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */

 /*
  * Description
  *   v1.0 - Minimum template to show how to use the Neural ART Embedded Client API
  *          Re-target of the printf function is out-of-scope.
  *
  *   For more information, see the embeded documentation:
  *
  *       [1] %X_CUBE_AI_DIR%/Documentation/index.html
  *
  *   X_CUBE_AI_DIR indicates the location where the X-CUBE-AI pack is installed
  *   typical : C:\Users\[user_name]\STM32Cube\Repository\STMicroelectronics\X-CUBE-AI\7.1.0
  */

#ifdef __cplusplus
 extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/

/* System headers */
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <string.h>

#include "app_x-cube-ai.h"
#include "main.h"

/* USER CODE BEGIN includes */
 // 输入量化参数
 #define INPUT_QUANT_SCALE 0.007812500f
 #define INPUT_QUANT_ZERO_POINT -1

 // 输出量化参数
 #define CONFIDENCE_QUANT_SCALE 0.003906250f
 #define CONFIDENCE_QUANT_ZERO_POINT -128
 #define BOXES_QUANT_SCALE 0.009008298f
 #define BOXES_QUANT_ZERO_POINT -56
#define INPUT_QUANT_SCALE_EMO 0.003921569f
#define INPUT_QUANT_ZERO_POINT_EMO -128
#define OUTPUT_QUANT_SCALE_EMO 0.00390625f
#define OUTPUT_QUANT_ZERO_POINT_EMO -128

#define NUM_ANCHORS 1118
#define NUM_CLASSES 2
#define MAX_DETECTIONS 50

typedef struct {
    int x1, y1, x2, y2;
    float confidence;
    int class_id;
} Detection;

const char* class_names[NUM_CLASSES] = {
    "BACKGROUND",
    "face"
};
Detection final_detections[MAX_DETECTIONS];
uint32_t total_frames_processed = 0;
uint32_t total_faces_detected = 0;
int num_faces=0;
/* USER CODE END includes */

/* Entry points --------------------------------------------------------------*/

LL_ATON_DECLARE_NAMED_NN_INSTANCE_AND_INTERFACE(face)
int8_t *buffer_in;
int8_t *buffer_out;
float DequantizeInt8(int8_t value, float scale, int zero_point);
int8_t QuantizeFloat(float value, float scale, int zero_point);
float CalculateIoU(Detection *box1, Detection *box2);
int HardNMS(Detection *detections, int count, float iou_threshold);
int PostProcessDetections(int8_t *output1, int8_t *output2, int frame_width, int frame_height,Detection *final_detections, float prob_threshold);
void set_clk_sleep_mode(void)
{
  /* Leave clocks enabled in Low Power modes */
  // Low-power clock enable misc
#if defined (CPU_IN_SECURE_STATE)
  __HAL_RCC_DBG_CLK_SLEEP_ENABLE();
#endif
  __HAL_RCC_XSPIPHYCOMP_CLK_SLEEP_ENABLE();

  // Low-power clock enable for memories
  __HAL_RCC_AXISRAM1_MEM_CLK_SLEEP_ENABLE();
  __HAL_RCC_AXISRAM2_MEM_CLK_SLEEP_ENABLE();
  __HAL_RCC_AXISRAM3_MEM_CLK_SLEEP_ENABLE();
  __HAL_RCC_AXISRAM4_MEM_CLK_SLEEP_ENABLE();
  __HAL_RCC_AXISRAM5_MEM_CLK_SLEEP_ENABLE();
  __HAL_RCC_AXISRAM6_MEM_CLK_SLEEP_ENABLE();
  __HAL_RCC_FLEXRAM_MEM_CLK_SLEEP_ENABLE();
  __HAL_RCC_CACHEAXIRAM_MEM_CLK_SLEEP_ENABLE();
  // LP clock AHB1: None
  // LP clock AHB2: None
  // LP clock AHB3
#if defined (CPU_IN_SECURE_STATE)
  __HAL_RCC_RIFSC_CLK_SLEEP_ENABLE();
  __HAL_RCC_RISAF_CLK_SLEEP_ENABLE();
  __HAL_RCC_IAC_CLK_SLEEP_ENABLE();
#endif
  // LP clock AHB4: None
  // LP clocks AHB5
  __HAL_RCC_XSPI1_CLK_SLEEP_ENABLE();
  __HAL_RCC_XSPI2_CLK_SLEEP_ENABLE();
  __HAL_RCC_CACHEAXI_CLK_SLEEP_ENABLE();
  __HAL_RCC_NPU_CLK_SLEEP_ENABLE();
  // LP clocks APB1: None
  // LP clocks APB2
  __HAL_RCC_USART1_CLK_SLEEP_ENABLE();
  // LP clocks APB4: None
  // LP clocks APB5: None
}

void MX_X_CUBE_AI_Init(void)
{
    __HAL_RCC_AXISRAM2_MEM_CLK_ENABLE();
    __HAL_RCC_AXISRAM3_MEM_CLK_ENABLE();
    __HAL_RCC_AXISRAM4_MEM_CLK_ENABLE();
    __HAL_RCC_AXISRAM5_MEM_CLK_ENABLE();
    __HAL_RCC_AXISRAM6_MEM_CLK_ENABLE();
    set_clk_sleep_mode();
    __HAL_RCC_NPU_CLK_ENABLE();
    __HAL_RCC_NPU_FORCE_RESET();
    __HAL_RCC_NPU_RELEASE_RESET();
    npu_cache_init();
    /* USER CODE BEGIN 5 */
    /* USER CODE END 5 */
}

void MX_X_CUBE_AI_Process(void)
{
    /* USER CODE BEGIN 6 */
  LL_ATON_RT_RetValues_t ll_aton_rt_ret = LL_ATON_RT_DONE;
  const LL_Buffer_InfoTypeDef * ibuffersInfos = NN_Interface_face.input_buffers_info();
  const LL_Buffer_InfoTypeDef * obuffersInfos = NN_Interface_face.output_buffers_info();
  buffer_in = (int8_t *)LL_Buffer_addr_start(&ibuffersInfos[0]);
  buffer_out = (int8_t *)LL_Buffer_addr_start(&obuffersInfos[0]);
  int8_t *out1 = (int8_t *)LL_Buffer_addr_start(&obuffersInfos[0]);
  int8_t *out2 = (int8_t *)LL_Buffer_addr_start(&obuffersInfos[1]);
  LL_ATON_RT_RuntimeInit();
  //printf("hello\n");
  // run 10 inferences
  for (int inferenceNb = 0; inferenceNb<1; ++inferenceNb) {
    /* ------------- */
    /* - Inference - */
    /* ------------- */
    /* Pre-process and fill the input buffer */
	 /* input 1/1          :   'Input_7_out_0', int8(1x3x120x160), 56.25 KBytes, QLinear(0.007812500,-1,int8), activations      
 output 1/2         :   'Quantize_245_out_0', int8(1x1118x2), 2.18 KBytes, QLinear(0.003906250,-128,int8), activations   
 output 2/2         :   'Quantize_233_out_0', int8(1x1118x4), 4.37 KBytes, QLinear(0.009008298,-56,int8), activations    */
    //_pre_process(buffer_in);
	  uint16_t *frame = (uint16_t *)0x34350000;
	  //printf("%d\n",frame[0]);
	      for(int y = 0; y < 120; y++)  // 目标高度120
	      {
	          for(int x = 0; x < 160; x++)  // 目标宽度160
	          {
	              uint16_t pixel = frame[y * 200 + (40 + x)];

	              // RGB565转RGB888
	              uint8_t r = (pixel >> 11) & 0x1F;
	              uint8_t g = (pixel >> 5) & 0x3F;
	              uint8_t b = pixel & 0x1F;

	              // 平滑扩展到8位
	              r = (r << 3) | (r >> 2);
	              g = (g << 2) | (g >> 4);
	              b = (b << 3) | (b >> 2);

	              // 2. 归一化 (0,255) → (-1,1)
	              float r_norm = (r - 127.0f) / 128.0f;
	              float g_norm = (g - 127.0f) / 128.0f;
	              float b_norm = (b - 127.0f) / 128.0f;

	              // 3. 转换为CHW格式并存储到模型输入缓冲区
	              // 输入格式: (1,3,120,160) - 批次=1, 通道=3, 高=120, 宽=160
	              int r_idx = 0 * 120 * 160 + y * 160 + x;      // R通道
	              int g_idx = 1 * 120 * 160 + y * 160 + x;      // G通道
	              int b_idx = 2 * 120 * 160 + y * 160 + x;      // B通道

	              buffer_in[r_idx] = QuantizeFloat(r_norm, INPUT_QUANT_SCALE, INPUT_QUANT_ZERO_POINT);
	              buffer_in[g_idx] = QuantizeFloat(g_norm, INPUT_QUANT_SCALE, INPUT_QUANT_ZERO_POINT);
	              buffer_in[b_idx] = QuantizeFloat(b_norm, INPUT_QUANT_SCALE, INPUT_QUANT_ZERO_POINT);
	          }
	      }

    /* Perform the inference */
    LL_ATON_RT_Init_Network(&NN_Instance_face);  // Initialize passed network instance object
    do {
      /* Execute first/next step */
      ll_aton_rt_ret = LL_ATON_RT_RunEpochBlock(&NN_Instance_face);
      /* Wait for next event */
      if (ll_aton_rt_ret == LL_ATON_RT_WFE) {
        LL_ATON_OSAL_WFE();
      }

    } while (ll_aton_rt_ret != LL_ATON_RT_DONE);
    /* 后处理 - 对应Python的predict函数 */
    int8_t *output1 = (int8_t *)out1;  // 置信度 [1,1118,2]
    int8_t *output2 = (int8_t *)out2;  // 边界框 [1,1118,4]

    // 检测人脸 (对应Python代码的predict函数调用)
    num_faces = PostProcessDetections(output1, output2, 200, 120,final_detections, 0.7f);

    // 更新统计信息
    total_frames_processed++;
    total_faces_detected += num_faces;

    // 输出结果 (对应Python代码的可视化部分)
    printf("=== Frame %lu ===\n", total_frames_processed);
    printf("Detected %d faces:\n", num_faces);

    for(int i = 0; i < num_faces; i++)
    {
        printf("%s %d: (%d,%d)-(%d,%d), confidence: %.2f\n",
               class_names[final_detections[i].class_id],
               i+1,
               final_detections[i].x1, final_detections[i].y1,
               final_detections[i].x2, final_detections[i].y2,
               final_detections[i].confidence);

        LL_ATON_DECLARE_NAMED_NN_INSTANCE_AND_INTERFACE(emotion)
        const LL_Buffer_InfoTypeDef * ibuffersInfosemo = NN_Interface_emotion.input_buffers_info();
        const LL_Buffer_InfoTypeDef * obuffersInfosemo = NN_Interface_emotion.output_buffers_info();
        buffer_in = (int8_t *)LL_Buffer_addr_start(&ibuffersInfosemo[0]);
        buffer_out = (int8_t *)LL_Buffer_addr_start(&obuffersInfosemo[0]);
        for (int inferenceNb = 0; inferenceNb<1; ++inferenceNb) {
          /* ------------- */
          /* - Inference - */
          /* ------------- */
          /* Pre-process and fill the input buffer */
          //_pre_process(buffer_in);
      	//input 1/1          :   'Input_12_out_0', int8(1x48x48x1), 2.25 KBytes, QLinear(0.003921569,-128,int8), activations
      	  // output 1/1: 'Quantize_105_out_0', int8(1x7), 7 Bytes, QLinear(0.003906250,-128,int8), activations   
      	    int start_x = (final_detections[i].x2 - final_detections[i].x1) / 2-24;
      	    int start_y = (final_detections[i].y2 - final_detections[i].y1) / 2-24;

      	    start_x=start_x>=0?start_x:0;
      	    start_y=start_y>=0?start_y:0;

      	    for(int y = 0; y < 48; y++) {  // 目标高度48
      	        for(int x = 0; x < 48; x++) {  // 目标宽度48
      	            // 从原始帧中获取像素
      	            uint16_t pixel = frame[(start_y + y) * 200 + (start_x + x)];

      	            // RGB565转RGB888
      	            uint8_t r = (pixel >> 11) & 0x1F;
      	            uint8_t g = (pixel >> 5) & 0x3F;
      	            uint8_t b = pixel & 0x1F;

      	            // 平滑扩展到8位
      	            r = (r << 3) | (r >> 2);
      	            g = (g << 2) | (g >> 4);
      	            b = (b << 3) | (b >> 2);

      	            // 转换为灰度值 (使用标准灰度转换公式)
      	            uint8_t gray = (uint8_t)(0.299f * r + 0.587f * g + 0.114f * b);

      	            // 归一化到 [0, 1] 范围
      	            float gray_norm = gray / 255.0f;

      	            // 计算在输入缓冲区中的索引
      	            // 输入格式: (1, 48, 48, 1) - 批次=1, 高=48, 宽=48, 通道=1
      	            int idx = y * 48 + x;

      	            // 量化并存储到模型输入缓冲区
      	            buffer_in[idx] = QuantizeFloat(gray_norm, INPUT_QUANT_SCALE_EMO, INPUT_QUANT_ZERO_POINT_EMO);
      	        }
      	    }

          /* Perform the inference */
      	  LL_ATON_RT_RuntimeDeInit();
      	 LL_ATON_RT_RuntimeInit();
          LL_ATON_RT_Init_Network(&NN_Instance_emotion);  // Initialize passed network instance object
          do {
            /* Execute first/next step */
            ll_aton_rt_ret = LL_ATON_RT_RunEpochBlock(&NN_Instance_emotion);
            /* Wait for next event */
            if (ll_aton_rt_ret == LL_ATON_RT_WFE) {
              LL_ATON_OSAL_WFE();
            }
          } while (ll_aton_rt_ret != LL_ATON_RT_DONE);
          //printf("hello\n");
          /* Post-process the output buffer */
          char predicted_emotion[32];
          float confidence;
          float predictions[7];

          // 定义情感类别标签
          const char* emotion_labels[7] = {
              "anger", "disgust", "fear", "happy", "sad", "surprised", "neutral"
          };

          // 反量化输出 (7个情感类别)
          for(int i = 0; i < 7; i++) {
              predictions[i] = DequantizeInt8(buffer_out[i], OUTPUT_QUANT_SCALE_EMO, OUTPUT_QUANT_ZERO_POINT_EMO);
          }

          // 找到最大概率的情感类别
          int max_index = 0;
          float max_value = predictions[0];

          for(int i = 1; i < 7; i++) {
              if(predictions[i] > max_value) {
                  max_value = predictions[i];
                  max_index = i;
              }
          }

          // 设置预测结果
          strcpy(predicted_emotion, emotion_labels[max_index]);
          confidence = predictions[max_index];

          // 输出结果 (对应Python代码的显示部分)
          printf("=== Emotion Recognition Result ===\n");
          printf("Face at (%d,%d)-(%d,%d)\n",
                 final_detections[0].x1, final_detections[0].y1,
                 final_detections[0].x2, final_detections[0].y2);
          printf("Predicted emotion: %s\n", predicted_emotion);
          printf("Confidence: %.2f%%\n", confidence * 100.0f);
          printf("All predictions:\n");
          for(int i = 0; i < 7; i++) {
              printf("  %s: %.2f%%\n", emotion_labels[i], predictions[i] * 100.0f);
          }
          printf("=================================\n");

          /* Invalidate the associated CPU cache region if requested */
          //_post_process(buffer_out);
          LL_ATON_RT_DeInit_Network(&NN_Instance_emotion);
          /* -------------------- */
          /* - End of Inference - */
          /* -------------------- */
        }

    }

    if(num_faces == 0) {
        printf("No faces detected\n");
    }

    printf("Total faces detected: %lu\n", total_faces_detected);
    printf("==================\n");
    /* Post-process the output buffer */
    /* Invalidate the associated CPU cache region if requested */
    //_post_process(buffer_out);
    LL_ATON_RT_DeInit_Network(&NN_Instance_face);
    /* -------------------- */
    /* - End of Inference - */
    /* -------------------- */
  }
  LL_ATON_RT_RuntimeDeInit();
    /* USER CODE END 6 */
}

//void MX_X_CUBE_AI_Process_emo(void)
//{
//    /* USER CODE BEGIN 6 */
//	//LL_ATON_DECLARE_NAMED_NN_INSTANCE_AND_INTERFACE(emotion)
//  LL_ATON_RT_RetValues_t ll_aton_rt_ret = LL_ATON_RT_DONE;
//  const LL_Buffer_InfoTypeDef * ibuffersInfos = NN_Interface_emotion.input_buffers_info();
//  const LL_Buffer_InfoTypeDef * obuffersInfos = NN_Interface_emotion.output_buffers_info();
//  buffer_in = (int8_t *)LL_Buffer_addr_start(&ibuffersInfos[0]);
//  buffer_out = (int8_t *)LL_Buffer_addr_start(&obuffersInfos[0]);
//  LL_ATON_RT_RuntimeInit();
//  // run 10 inferences
//  for (int inferenceNb = 0; inferenceNb<1; ++inferenceNb) {
//    /* ------------- */
//    /* - Inference - */
//    /* ------------- */
//    /* Pre-process and fill the input buffer */
//    //_pre_process(buffer_in);
//	//input 1/1          :   'Input_12_out_0', int8(1x48x48x1), 2.25 KBytes, QLinear(0.003921569,-128,int8), activations
//	  // output 1/1: 'Quantize_105_out_0', int8(1x7), 7 Bytes, QLinear(0.003906250,-128,int8), activations   
//	  uint16_t *frame = (uint16_t *)0x342BD000;
//	    int start_x = (final_detections[0].x2 - final_detections[0].x1) / 2-24;
//	    int start_y = (final_detections[0].y2 - final_detections[0].y1) / 2-24;
//
//	    start_x=start_x>=0?start_x:0;
//	    start_y=start_y>=0?start_y:0;
//
//	    for(int y = 0; y < 48; y++) {  // 目标高度48
//	        for(int x = 0; x < 48; x++) {  // 目标宽度48
//	            // 从原始帧中获取像素
//	            uint16_t pixel = frame[(start_y + y) * 200 + (start_x + x)];
//
//	            // RGB565转RGB888
//	            uint8_t r = (pixel >> 11) & 0x1F;
//	            uint8_t g = (pixel >> 5) & 0x3F;
//	            uint8_t b = pixel & 0x1F;
//
//	            // 平滑扩展到8位
//	            r = (r << 3) | (r >> 2);
//	            g = (g << 2) | (g >> 4);
//	            b = (b << 3) | (b >> 2);
//
//	            // 转换为灰度值 (使用标准灰度转换公式)
//	            uint8_t gray = (uint8_t)(0.299f * r + 0.587f * g + 0.114f * b);
//
//	            // 归一化到 [0, 1] 范围
//	            float gray_norm = gray / 255.0f;
//
//	            // 计算在输入缓冲区中的索引
//	            // 输入格式: (1, 48, 48, 1) - 批次=1, 高=48, 宽=48, 通道=1
//	            int idx = y * 48 + x;
//
//	            // 量化并存储到模型输入缓冲区
//	            buffer_in[idx] = QuantizeFloat(gray_norm, INPUT_QUANT_SCALE_EMO, INPUT_QUANT_ZERO_POINT_EMO);
//	        }
//	    }
//    /* Perform the inference */
//    LL_ATON_RT_Init_Network(&NN_Instance_emotion);  // Initialize passed network instance object
//    do {
//      /* Execute first/next step */
//      ll_aton_rt_ret = LL_ATON_RT_RunEpochBlock(&NN_Instance_emotion);
//      /* Wait for next event */
//      if (ll_aton_rt_ret == LL_ATON_RT_WFE) {
//        LL_ATON_OSAL_WFE();
//      }
//    } while (ll_aton_rt_ret != LL_ATON_RT_DONE);
//    /* Post-process the output buffer */
//    char predicted_emotion[32];
//    float confidence;
//    float predictions[7];
//
//    // 定义情感类别标签
//    const char* emotion_labels[7] = {
//        "anger", "disgust", "fear", "happy", "sad", "surprised", "neutral"
//    };
//
//    // 反量化输出 (7个情感类别)
//    for(int i = 0; i < 7; i++) {
//        predictions[i] = DequantizeInt8(buffer_out[i], OUTPUT_QUANT_SCALE_EMO, OUTPUT_QUANT_ZERO_POINT_EMO);
//    }
//
//    // 找到最大概率的情感类别
//    int max_index = 0;
//    float max_value = predictions[0];
//
//    for(int i = 1; i < 7; i++) {
//        if(predictions[i] > max_value) {
//            max_value = predictions[i];
//            max_index = i;
//        }
//    }
//
//    // 设置预测结果
//    strcpy(predicted_emotion, emotion_labels[max_index]);
//    confidence = predictions[max_index];
//
//    // 输出结果 (对应Python代码的显示部分)
//    printf("=== Emotion Recognition Result ===\n");
//    printf("Face at (%d,%d)-(%d,%d)\n",
//           final_detections[0].x1, final_detections[0].y1,
//           final_detections[0].x2, final_detections[0].y2);
//    printf("Predicted emotion: %s\n", predicted_emotion);
//    printf("Confidence: %.2f%%\n", confidence * 100.0f);
//    printf("All predictions:\n");
//    for(int i = 0; i < 7; i++) {
//        printf("  %s: %.2f%%\n", emotion_labels[i], predictions[i] * 100.0f);
//    }
//    printf("=================================\n");
//
//    /* Invalidate the associated CPU cache region if requested */
//    //_post_process(buffer_out);
//    LL_ATON_RT_DeInit_Network(&NN_Instance_emotion);
//    /* -------------------- */
//    /* - End of Inference - */
//    /* -------------------- */
//  }
//  LL_ATON_RT_RuntimeDeInit();
//    /* USER CODE END 6 */
//}

int8_t QuantizeFloat(float value, float scale, int zero_point)
{
    // quantized_value = (value / scale) + zero_point
    float quantized = (value / scale) + zero_point;

    // 限制到INT8范围 [-128, 127]
    if (quantized > 127.0f) quantized = 127.0f;
    if (quantized < -128.0f) quantized = -128.0f;

    return (int8_t)quantized;
}

// INT8反量化为浮点数
float DequantizeInt8(int8_t value, float scale, int zero_point)
{
    // float_value = (quantized_value - zero_point) * scale
    return (float)(value - zero_point) * scale;
}

// IOU计算 (对应Python的iou_of函数)
float CalculateIoU(Detection *box1, Detection *box2)
{
    int overlap_x1 = (box1->x1 > box2->x1) ? box1->x1 : box2->x1;
    int overlap_y1 = (box1->y1 > box2->y1) ? box1->y1 : box2->y1;
    int overlap_x2 = (box1->x2 < box2->x2) ? box1->x2 : box2->x2;
    int overlap_y2 = (box1->y2 < box2->y2) ? box1->y2 : box2->y2;

    if(overlap_x1 >= overlap_x2 || overlap_y1 >= overlap_y2)
        return 0.0f;

    int overlap_area = (overlap_x2 - overlap_x1) * (overlap_y2 - overlap_y1);
    int area1 = (box1->x2 - box1->x1) * (box1->y2 - box1->y1);
    int area2 = (box2->x2 - box2->x1) * (box2->y2 - box2->y1);
    int union_area = area1 + area2 - overlap_area;

    return (float)overlap_area / (float)union_area;
}

// NMS处理 (对应Python的hard_nms函数)
int HardNMS(Detection *detections, int count, float iou_threshold)
{
    // 按置信度降序排序 (对应Python的np.argsort)
    for(int i = 0; i < count - 1; i++)
    {
        for(int j = i + 1; j < count; j++)
        {
            if(detections[i].confidence < detections[j].confidence)
            {
                Detection temp = detections[i];
                detections[i] = detections[j];
                detections[j] = temp;
            }
        }
    }

    // NMS筛选 (对应Python的while循环)
    int final_count = 0;
    for(int i = 0; i < count; i++)
    {
        int keep = 1;
        for(int j = 0; j < final_count; j++)
        {
            float iou = CalculateIoU(&detections[i], &detections[j]);
            if(iou > iou_threshold)
            {
                keep = 0;
                break;
            }
        }

        if(keep)
        {
            if(final_count != i)
            {
                detections[final_count] = detections[i];
            }
            final_count++;
        }
    }

    return final_count;
}

// 后处理函数 (对应Python的predict函数)
int PostProcessDetections(int8_t *output1, int8_t *output2, int frame_width, int frame_height,
                         Detection *final_detections, float prob_threshold)
{
    int detection_count = 0;

    // 处理每个锚框 (对应Python的for class_index循环)
    for(int i = 0; i < NUM_ANCHORS && detection_count < MAX_DETECTIONS; i++)
    {
        // 反量化置信度 - 获取人脸类别(索引1)的置信度
        int8_t face_conf_raw = output1[i * NUM_CLASSES + 1];
        float face_confidence = DequantizeInt8(face_conf_raw, CONFIDENCE_QUANT_SCALE, CONFIDENCE_QUANT_ZERO_POINT);

        // 置信度阈值过滤 (对应Python的mask = probs > prob_threshold)
        if(face_confidence <= prob_threshold)
            continue;

        // 反量化边界框坐标
        int8_t x1_raw = output2[i * 4 + 0];
        int8_t y1_raw = output2[i * 4 + 1];
        int8_t x2_raw = output2[i * 4 + 2];
        int8_t y2_raw = output2[i * 4 + 3];

        float x1_norm = DequantizeInt8(x1_raw, BOXES_QUANT_SCALE, BOXES_QUANT_ZERO_POINT);
        float y1_norm = DequantizeInt8(y1_raw, BOXES_QUANT_SCALE, BOXES_QUANT_ZERO_POINT);
        float x2_norm = DequantizeInt8(x2_raw, BOXES_QUANT_SCALE, BOXES_QUANT_ZERO_POINT);
        float y2_norm = DequantizeInt8(y2_raw, BOXES_QUANT_SCALE, BOXES_QUANT_ZERO_POINT);

        // 转换为像素坐标 (对应Python的坐标转换部分)
        int x1 = (int)(x1_norm * frame_width);
        int y1 = (int)(y1_norm * frame_height);
        int x2 = (int)(x2_norm * frame_width);
        int y2 = (int)(y2_norm * frame_height);

        // 边界检查
        if(x1 < 0) x1 = 0;
        if(y1 < 0) y1 = 0;
        if(x2 >= frame_width) x2 = frame_width - 1;
        if(y2 >= frame_height) y2 = frame_height - 1;

        // 检查边界框有效性
        if(x2 <= x1 || y2 <= y1)
            continue;

        // 保存检测结果
        final_detections[detection_count].x1 = x1;
        final_detections[detection_count].y1 = y1;
        final_detections[detection_count].x2 = x2;
        final_detections[detection_count].y2 = y2;
        final_detections[detection_count].confidence = face_confidence;
        final_detections[detection_count].class_id = 1;  // face类别

        detection_count++;
    }

    // 执行NMS (对应Python的hard_nms调用)
    if(detection_count > 0)
    {
        detection_count = HardNMS(final_detections, detection_count, 0.3f);
    }

    return detection_count;
}

#ifdef __cplusplus
}
#endif
