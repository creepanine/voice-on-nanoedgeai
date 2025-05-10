################################################################################
# 自动生成的文件。不要编辑！
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Middlewares/isp_algo.c \
../Middlewares/isp_core.c \
../Middlewares/isp_services.c 

OBJS += \
./Middlewares/isp_algo.o \
./Middlewares/isp_core.o \
./Middlewares/isp_services.o 

C_DEPS += \
./Middlewares/isp_algo.d \
./Middlewares/isp_core.d \
./Middlewares/isp_services.d 


# Each subdirectory must supply rules for building sources it contributes
Middlewares/%.o Middlewares/%.su Middlewares/%.cyclo: ../Middlewares/%.c Middlewares/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m55 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32N657xx -c -I../Inc -I../../Drivers/STM32N6xx_HAL_Driver/Inc -I../../Drivers/CMSIS/Device/ST/STM32N6xx/Include -I../../Drivers/STM32N6xx_HAL_Driver/Inc/Legacy -I../../Drivers/CMSIS/Include -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/Middlewares" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/ISP_evision/evision" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/ISP_evision" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/Components/imx335" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/Components/STM32N6570-DK" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/Components/Common" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -mcmse -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Middlewares

clean-Middlewares:
	-$(RM) ./Middlewares/isp_algo.cyclo ./Middlewares/isp_algo.d ./Middlewares/isp_algo.o ./Middlewares/isp_algo.su ./Middlewares/isp_core.cyclo ./Middlewares/isp_core.d ./Middlewares/isp_core.o ./Middlewares/isp_core.su ./Middlewares/isp_services.cyclo ./Middlewares/isp_services.d ./Middlewares/isp_services.o ./Middlewares/isp_services.su

.PHONY: clean-Middlewares

