################################################################################
# 自动生成的文件。不要编辑！
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/main.c \
../Core/Src/stm32n6xx_hal_msp.c \
../Core/Src/stm32n6xx_it.c \
../Core/Src/syscalls.c \
../Core/Src/sysmem.c \
../Core/Src/system_stm32n6xx_fsbl.c 

OBJS += \
./Core/Src/main.o \
./Core/Src/stm32n6xx_hal_msp.o \
./Core/Src/stm32n6xx_it.o \
./Core/Src/syscalls.o \
./Core/Src/sysmem.o \
./Core/Src/system_stm32n6xx_fsbl.o 

C_DEPS += \
./Core/Src/main.d \
./Core/Src/stm32n6xx_hal_msp.d \
./Core/Src/stm32n6xx_it.d \
./Core/Src/syscalls.d \
./Core/Src/sysmem.d \
./Core/Src/system_stm32n6xx_fsbl.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/%.o Core/Src/%.su Core/Src/%.cyclo: ../Core/Src/%.c Core/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m55 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32N657xx -c -I../Core/Inc -I../../Drivers/STM32N6xx_HAL_Driver/Inc -I../../Drivers/CMSIS/Device/ST/STM32N6xx/Include -I../../Drivers/STM32N6xx_HAL_Driver/Inc/Legacy -I../../Drivers/CMSIS/Include -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/Common" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/rk050hr18" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/STM32N6570-DK" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Components/imx335" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Util/Fonts" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/Util/lcd" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/ISP_LIB" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/evision/header" -I"D:/Users/realw/Documents/voice-on-nanoedgeai/LCD1/FSBL/evision/lib" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -mcmse -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src

clean-Core-2f-Src:
	-$(RM) ./Core/Src/main.cyclo ./Core/Src/main.d ./Core/Src/main.o ./Core/Src/main.su ./Core/Src/stm32n6xx_hal_msp.cyclo ./Core/Src/stm32n6xx_hal_msp.d ./Core/Src/stm32n6xx_hal_msp.o ./Core/Src/stm32n6xx_hal_msp.su ./Core/Src/stm32n6xx_it.cyclo ./Core/Src/stm32n6xx_it.d ./Core/Src/stm32n6xx_it.o ./Core/Src/stm32n6xx_it.su ./Core/Src/syscalls.cyclo ./Core/Src/syscalls.d ./Core/Src/syscalls.o ./Core/Src/syscalls.su ./Core/Src/sysmem.cyclo ./Core/Src/sysmem.d ./Core/Src/sysmem.o ./Core/Src/sysmem.su ./Core/Src/system_stm32n6xx_fsbl.cyclo ./Core/Src/system_stm32n6xx_fsbl.d ./Core/Src/system_stm32n6xx_fsbl.o ./Core/Src/system_stm32n6xx_fsbl.su

.PHONY: clean-Core-2f-Src

