################################################################################
# 自动生成的文件。不要编辑！
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Util/Fonts/font12.c \
../Util/Fonts/font16.c \
../Util/Fonts/font20.c \
../Util/Fonts/font24.c \
../Util/Fonts/font8.c 

OBJS += \
./Util/Fonts/font12.o \
./Util/Fonts/font16.o \
./Util/Fonts/font20.o \
./Util/Fonts/font24.o \
./Util/Fonts/font8.o 

C_DEPS += \
./Util/Fonts/font12.d \
./Util/Fonts/font16.d \
./Util/Fonts/font20.d \
./Util/Fonts/font24.d \
./Util/Fonts/font8.d 


# Each subdirectory must supply rules for building sources it contributes
Util/Fonts/%.o Util/Fonts/%.su Util/Fonts/%.cyclo: ../Util/Fonts/%.c Util/Fonts/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m55 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32N657xx -c -I../Core/Inc -I../../Drivers/STM32N6xx_HAL_Driver/Inc -I../../Drivers/CMSIS/Device/ST/STM32N6xx/Include -I../../Drivers/STM32N6xx_HAL_Driver/Inc/Legacy -I../../Drivers/CMSIS/Include -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/Common" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/rk050hr18" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/STM32N6570-DK" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/imx335" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Util/Fonts" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Util/lcd" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/ISP_LIB" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/evision/header" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/evision/lib" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -mcmse -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Util-2f-Fonts

clean-Util-2f-Fonts:
	-$(RM) ./Util/Fonts/font12.cyclo ./Util/Fonts/font12.d ./Util/Fonts/font12.o ./Util/Fonts/font12.su ./Util/Fonts/font16.cyclo ./Util/Fonts/font16.d ./Util/Fonts/font16.o ./Util/Fonts/font16.su ./Util/Fonts/font20.cyclo ./Util/Fonts/font20.d ./Util/Fonts/font20.o ./Util/Fonts/font20.su ./Util/Fonts/font24.cyclo ./Util/Fonts/font24.d ./Util/Fonts/font24.o ./Util/Fonts/font24.su ./Util/Fonts/font8.cyclo ./Util/Fonts/font8.d ./Util/Fonts/font8.o ./Util/Fonts/font8.su

.PHONY: clean-Util-2f-Fonts

