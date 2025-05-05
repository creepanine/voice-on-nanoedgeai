################################################################################
# 自动生成的文件。不要编辑！
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../ISP_LIB/isp_algo.c \
../ISP_LIB/isp_core.c \
../ISP_LIB/isp_services.c 

OBJS += \
./ISP_LIB/isp_algo.o \
./ISP_LIB/isp_core.o \
./ISP_LIB/isp_services.o 

C_DEPS += \
./ISP_LIB/isp_algo.d \
./ISP_LIB/isp_core.d \
./ISP_LIB/isp_services.d 


# Each subdirectory must supply rules for building sources it contributes
ISP_LIB/%.o ISP_LIB/%.su ISP_LIB/%.cyclo: ../ISP_LIB/%.c ISP_LIB/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m55 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32N657xx -c -I../Core/Inc -I../../Drivers/STM32N6xx_HAL_Driver/Inc -I../../Drivers/CMSIS/Device/ST/STM32N6xx/Include -I../../Drivers/STM32N6xx_HAL_Driver/Inc/Legacy -I../../Drivers/CMSIS/Include -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/Common" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/rk050hr18" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/STM32N6570-DK" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/imx335" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Util/Fonts" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Util/lcd" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/ISP_LIB" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/evision/header" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/evision/lib" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -mcmse -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-ISP_LIB

clean-ISP_LIB:
	-$(RM) ./ISP_LIB/isp_algo.cyclo ./ISP_LIB/isp_algo.d ./ISP_LIB/isp_algo.o ./ISP_LIB/isp_algo.su ./ISP_LIB/isp_core.cyclo ./ISP_LIB/isp_core.d ./ISP_LIB/isp_core.o ./ISP_LIB/isp_core.su ./ISP_LIB/isp_services.cyclo ./ISP_LIB/isp_services.d ./ISP_LIB/isp_services.o ./ISP_LIB/isp_services.su

.PHONY: clean-ISP_LIB

