################################################################################
# 自动生成的文件。不要编辑！
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Components/STM32N6570-DK/stm32n6570_discovery.c \
../Components/STM32N6570-DK/stm32n6570_discovery_bus.c 

OBJS += \
./Components/STM32N6570-DK/stm32n6570_discovery.o \
./Components/STM32N6570-DK/stm32n6570_discovery_bus.o 

C_DEPS += \
./Components/STM32N6570-DK/stm32n6570_discovery.d \
./Components/STM32N6570-DK/stm32n6570_discovery_bus.d 


# Each subdirectory must supply rules for building sources it contributes
Components/STM32N6570-DK/%.o Components/STM32N6570-DK/%.su Components/STM32N6570-DK/%.cyclo: ../Components/STM32N6570-DK/%.c Components/STM32N6570-DK/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m55 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32N657xx -c -I../Inc -I../../Drivers/STM32N6xx_HAL_Driver/Inc -I../../Drivers/CMSIS/Device/ST/STM32N6xx/Include -I../../Drivers/STM32N6xx_HAL_Driver/Inc/Legacy -I../../Drivers/CMSIS/Include -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/Middlewares" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/ISP_evision/evision" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/ISP_evision" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/Components/imx335" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/Components/STM32N6570-DK" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/Components/Common" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -mcmse -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Components-2f-STM32N6570-2d-DK

clean-Components-2f-STM32N6570-2d-DK:
	-$(RM) ./Components/STM32N6570-DK/stm32n6570_discovery.cyclo ./Components/STM32N6570-DK/stm32n6570_discovery.d ./Components/STM32N6570-DK/stm32n6570_discovery.o ./Components/STM32N6570-DK/stm32n6570_discovery.su ./Components/STM32N6570-DK/stm32n6570_discovery_bus.cyclo ./Components/STM32N6570-DK/stm32n6570_discovery_bus.d ./Components/STM32N6570-DK/stm32n6570_discovery_bus.o ./Components/STM32N6570-DK/stm32n6570_discovery_bus.su

.PHONY: clean-Components-2f-STM32N6570-2d-DK

