// COMPENG 2DX3 Studio 5 Code Template
// Caylia Bonnick
// Student Number: 400373187
// Second Least Significant Digit: 8
// March 12, 2024

#include <stdint.h>   
#include "tm4c1294ncpdt.h"   
#include "Systick.h"   
#include "PLL.h"   


// Function to initialize Port E
void PortE_Init(void) {
    SYSCTL_RCGCGPIO_R |= SYSCTL_RCGCGPIO_R4;  // Activate the clock for Port E
    while((SYSCTL_PRGPIO_R & SYSCTL_PRGPIO_R4) == 0) {};  // Wait for the clock to stabilize
  
    GPIO_PORTE_DIR_R = 0b00000011;  // Enable PE0 and PE1 as outputs
    GPIO_PORTE_DEN_R = 0b00000011;  // Enable PE0 and PE1 as digital pins
    return;
}

// Function to initialize Port M
void PortM_Init(void) {
    SYSCTL_RCGCGPIO_R |= SYSCTL_RCGCGPIO_R11;  // Activate the clock for Port M
    while((SYSCTL_PRGPIO_R & SYSCTL_PRGPIO_R11) == 0) {};  // Wait for the clock to stabilize
    
    GPIO_PORTM_DIR_R = 0b00000000;  // Make PM0:PM1 inputs, reading if the button is pressed or not
    GPIO_PORTM_DEN_R = 0b00001111;  // Enable PM0:PM1
    GPIO_PORTM_PUR_R = 0b00001111;  // Enable the pull-up resistors for PM3:PM0
    return;
}

// Function to initialize Port N (Turns on D2, D1)
void PortN_Init(void) {
    SYSCTL_RCGCGPIO_R |= SYSCTL_RCGCGPIO_R12;  // Activate the clock for Port N
    while((SYSCTL_PRGPIO_R & SYSCTL_PRGPIO_R12) == 0) {};  // Wait for the clock to stabilize
    
    GPIO_PORTN_DIR_R = 0b00000011;  // Make PN0 and PN1 output
    GPIO_PORTN_DEN_R = 0b00000011;  // Enable PN0 and PN1
    return;
}

// Function to initialize Port F (Turns on D3, D4)
void PortF_Init(void) {
    SYSCTL_RCGCGPIO_R |= SYSCTL_RCGCGPIO_R5;  // Activate the clock for Port F
    while((SYSCTL_PRGPIO_R & SYSCTL_PRGPIO_R5) == 0) {};  // Wait for the clock to stabilize
    
    GPIO_PORTF_DIR_R = 0b00010001;  // Make PF0 and PF4 outputs, to turn on LEDs
    GPIO_PORTF_DEN_R = 0b00010001;  // Enable PF0 and PF4
    return;
}

// Function to initialize Port H
void PortH_Init(void) {
    SYSCTL_RCGCGPIO_R |= SYSCTL_RCGCGPIO_R7;  // Activate clock for Port H
    while((SYSCTL_PRGPIO_R & SYSCTL_PRGPIO_R7) == 0) {};  // Wait for the clock to stabilize
    
    GPIO_PORTH_DIR_R |= 0xFF;  // Make all bits of Port H as output
    GPIO_PORTH_DEN_R |= 0xFF;  // Enable all pins of Port H as digital pins
    return;
}

// Function to control the motor rotation
void spin(int direction, int angle, int position) {  // 1 = forward direction, 0 = reverse direction
    if (direction == 1) {  // Check if the direction is forward (clockwise)
 
        GPIO_PORTH_DATA_R = 0b00001100;  // Set PH1 and PH2 to rotate the motor
        SysTick_Wait10ms(1);   
        GPIO_PORTH_DATA_R = 0b00000110;  // Set PH2 and PH3 to rotate the motor
        SysTick_Wait10ms(1);   
        GPIO_PORTH_DATA_R = 0b00000011;  // Set PH3 and PH4 to rotate the motor
        SysTick_Wait10ms(1);   
        GPIO_PORTH_DATA_R = 0b00001001;  // Set PH1 and PH4 to rotate the motor
        SysTick_Wait10ms(1);   
    }
    else { // Rotation sequence for reverse direction
         
        GPIO_PORTH_DATA_R = 0b00001001;  // Set PH1 and PH4 to rotate the motor
        SysTick_Wait10ms(1);   
        GPIO_PORTH_DATA_R = 0b00000011;  // Set PH3 and PH4 to rotate the motor
        SysTick_Wait10ms(1);   
        GPIO_PORTH_DATA_R = 0b00000110;  // Set PH2 and PH3 to rotate the motor
        SysTick_Wait10ms(1);   
        GPIO_PORTH_DATA_R = 0b00001100;  // Set PH1 and PH2 to rotate the motor
        SysTick_Wait10ms(1);   
    }
    
    if (angle) {   
        if (position % 64 == 0) {  // Check if the position is at a 45-degree angle step
            GPIO_PORTN_DATA_R = 0b1;  // Turn on D2 to indicate the angle step
            SysTick_Wait10ms(5);   
            GPIO_PORTN_DATA_R = 0b10;  // Turn off D2
        }
        else {
            GPIO_PORTN_DATA_R = 0b10;  // Keep D2 off for non-angle positions
        }
    }
    else { 
        if (position % 64 == 0) {  // Check if the position is at a 45-degree angle step
            GPIO_PORTN_DATA_R = 0b00000001;  // Turn on D2 [PN0] to indicate the angle step
            SysTick_Wait10ms(1);   
            GPIO_PORTN_DATA_R = 0b0;  // Turn off D2 [PN0]
        }
    }
}


int main(void) {
    PortE_Init();
    PortM_Init();
    PortN_Init();
    PortF_Init();
    PLL_Init();
    SysTick_Init();
    PortH_Init();

    int operation = 0;  // Motor operation (0 = stopped, 1 = running)
    int prev_operation = 0;  // Stores previous operation state
    int direction = 0;  // Store motor direction (0 = reverse, 1 = forward)
    int angle = 0;  // To enable/disable angle mode (0 = disabled, 1 = enabled)
    int position = 0;  // Tto track motor position
    int motor_on = 0;  // Motor power state (0 = off, 1 = on)
    int new_motor_on = 0;  // To indicate change in motor power state

    while (1) {
        // BUTTON OPERATION [PM0]
        // Start/Stop
        if ((GPIO_PORTM_DATA_R & 0b00000001) == 0) {
            if (prev_operation != 0) {  // If previous operation is different
                operation ^= 1;  // Toggle motor operation flag
                motor_on = operation;  // Update motor power state
                if (!motor_on) {  // If motor was stopped mid-rotation
                    position = 0;  // Reset position to start new rotation
                }
                prev_operation = 0;  // Update previous operation flag
            }
            while ((GPIO_PORTM_DATA_R & 0b00000001) == 0) {}  // Wait until button is released
        } else {
            prev_operation = 1;  // Set previous operation flag
        } 

        // Motor Control
        if (motor_on) {
            GPIO_PORTN_DATA_R |= 0b00000010;  // Turn on D1 [PN1]
        } else {
            GPIO_PORTN_DATA_R &= ~0b00000010;  // Turn off D1 [PN1]
        }

        if (operation && motor_on && (new_motor_on != motor_on)) { // Start a new rotation sequence
            position = 0;  // Reset position to start new rotation
            new_motor_on = motor_on;  // Update new motor power state
        }

        if (operation && motor_on && (position < 512)) { // Check if motor operation, power state, and position are within limits
            spin(direction, angle, position);  // Perform motor rotation
            position++;  
        }
    }
}