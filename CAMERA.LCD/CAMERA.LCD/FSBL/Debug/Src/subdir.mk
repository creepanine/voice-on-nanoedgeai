################################################################################
# 自动生成的文件。不要编辑！
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Src/main.c \
../Src/stm32n6xx_hal_msp.c \
../Src/stm32n6xx_it.c \
../Src/syscalls.c \
../Src/sysmem.c \
../Src/system_stm32n6xx_fsbl.c 

OBJS += \
./Src/main.o \
./Src/stm32n6xx_hal_msp.o \
./Src/stm32n6xx_it.o \
./Src/syscalls.o \
./Src/sysmem.o \
./Src/system_stm32n6xx_fsbl.o 

C_DEPS += \
./Src/main.d \
./Src/stm32n6xx_hal_msp.d \
./Src/stm32n6xx_it.d \
./Src/syscalls.d \
./Src/sysmem.d \
./Src/system_stm32n6xx_fsbl.d 


# Each subdirectory must supply rules for building sources it contributes
Src/%.o Src/%.su Src/%.cyclo: ../Src/%.c Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m55 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32N657xx -c -I../Inc -I../../Drivers/STM32N6xx_HAL_Driver/Inc -I../../Drivers/CMSIS/Device/ST/STM32N6xx/Include -I../../Drivers/STM32N6xx_HAL_Driver/Inc/Legacy -I../../Drivers/CMSIS/Include -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/Middlewares" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/ISP_evision/evision" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/ISP_evision" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/Components/imx335" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/Components/STM32N6570-DK" -I"D:/Users/realw/Documents/cubezip/CAMERA.LCD/CAMERA.LCD/FSBL/Components/Common" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -mcmse -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Src

clean-Src:
	-$(RM) ./Src/main.cyclo ./Src/main.d ./Src/main.o ./Src/main.su ./Src/stm32n6xx_hal_msp.cyclo ./Src/stm32n6xx_hal_msp.d ./Src/stm32n6xx_hal_msp.o ./Src/stm32n6xx_hal_msp.su ./Src/stm32n6xx_it.cyclo ./Src/stm32n6xx_it.d ./Src/stm32n6xx_it.o ./Src/stm32n6xx_it.su ./Src/syscalls.cyclo ./Src/syscalls.d ./Src/syscalls.o ./Src/syscalls.su ./Src/sysmem.cyclo ./Src/sysmem.d ./Src/sysmem.o ./Src/sysmem.su ./Src/system_stm32n6xx_fsbl.cyclo ./Src/system_stm32n6xx_fsbl.d ./Src/system_stm32n6xx_fsbl.o ./Src/system_stm32n6xx_fsbl.su

.PHONY: clean-Src

