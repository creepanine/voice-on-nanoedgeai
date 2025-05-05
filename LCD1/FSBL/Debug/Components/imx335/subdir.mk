################################################################################
# 自动生成的文件。不要编辑！
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Components/imx335/imx335.c \
../Components/imx335/imx335_reg.c 

OBJS += \
./Components/imx335/imx335.o \
./Components/imx335/imx335_reg.o 

C_DEPS += \
./Components/imx335/imx335.d \
./Components/imx335/imx335_reg.d 


# Each subdirectory must supply rules for building sources it contributes
Components/imx335/%.o Components/imx335/%.su Components/imx335/%.cyclo: ../Components/imx335/%.c Components/imx335/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m55 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32N657xx -c -I../Core/Inc -I../../Drivers/STM32N6xx_HAL_Driver/Inc -I../../Drivers/CMSIS/Device/ST/STM32N6xx/Include -I../../Drivers/STM32N6xx_HAL_Driver/Inc/Legacy -I../../Drivers/CMSIS/Include -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/Common" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/rk050hr18" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/STM32N6570-DK" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/imx335" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Util/Fonts" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Util/lcd" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/ISP_LIB" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/evision/header" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/evision/lib" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -mcmse -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Components-2f-imx335

clean-Components-2f-imx335:
	-$(RM) ./Components/imx335/imx335.cyclo ./Components/imx335/imx335.d ./Components/imx335/imx335.o ./Components/imx335/imx335.su ./Components/imx335/imx335_reg.cyclo ./Components/imx335/imx335_reg.d ./Components/imx335/imx335_reg.o ./Components/imx335/imx335_reg.su

.PHONY: clean-Components-2f-imx335

