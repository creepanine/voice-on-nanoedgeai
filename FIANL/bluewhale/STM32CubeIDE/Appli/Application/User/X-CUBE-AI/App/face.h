/**
  ******************************************************************************
  * @file    face.h
  * @author  STEdgeAI
  * @date    2025-07-02 14:52:54
  * @brief   Minimal description of the generated c-implemention of the network
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  ******************************************************************************
  */
#ifndef LL_ATON_FACE_H
#define LL_ATON_FACE_H

/******************************************************************************/
#define LL_ATON_FACE_C_MODEL_NAME        "face"
#define LL_ATON_FACE_ORIGIN_MODEL_NAME   "facedect"

/************************** USER ALLOCATED IOs ********************************/
// No user allocated inputs
// No user allocated outputs

/************************** INPUTS ********************************************/
#define LL_ATON_FACE_IN_NUM        (1)    // Total number of input buffers
// Input buffer 1 -- Input_7_out_0
#define LL_ATON_FACE_IN_1_ALIGNMENT   (32)
#define LL_ATON_FACE_IN_1_SIZE_BYTES  (57600)

/************************** OUTPUTS *******************************************/
#define LL_ATON_FACE_OUT_NUM        (2)    // Total number of output buffers
// Output buffer 1 -- Quantize_245_out_0
#define LL_ATON_FACE_OUT_1_ALIGNMENT   (32)
#define LL_ATON_FACE_OUT_1_SIZE_BYTES  (2236)
// Output buffer 2 -- Quantize_233_out_0
#define LL_ATON_FACE_OUT_2_ALIGNMENT   (32)
#define LL_ATON_FACE_OUT_2_SIZE_BYTES  (4472)

#endif /* LL_ATON_FACE_H */
