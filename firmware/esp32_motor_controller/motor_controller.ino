/*
 * DDSM210 Differential Drive Controller
 * Receives "linear,angular" over Serial
 * Example: 0.5,0.2
 */

#include "ddsm_ctrl.h"

DDSM_CTRL dc;

// ------------------------
// UART to DDSM
// ------------------------
#define DDSM_RX 18
#define DDSM_TX 19

// ------------------------
// Motor IDs
// ------------------------
#define LEFT_FRONT   1
#define LEFT_REAR    3
#define RIGHT_FRONT  4
#define RIGHT_REAR   2

// ------------------------
// Robot Parameters
// ------------------------
const float WHEEL_RADIUS = 0.10;   // meters
const float WHEEL_BASE   = 0.45;   // meters

String serialBuffer;

void setup()
{
    Serial.begin(115200);

    Serial1.begin(DDSM_BAUDRATE, SERIAL_8N1, DDSM_RX, DDSM_TX);

    dc.pSerial = &Serial1;
    dc.set_ddsm_type(210);
    dc.clear_ddsm_buffer();
}

void driveRobot(float linear, float angular)
{
    // Differential drive kinematics
    float leftVel  = linear - (angular * WHEEL_BASE * 0.5);
    float rightVel = linear + (angular * WHEEL_BASE * 0.5);

    // Convert m/s -> RPM
    float leftRPM =
        (leftVel / (2.0 * PI * WHEEL_RADIUS)) * 60.0;

    float rightRPM =
        (rightVel / (2.0 * PI * WHEEL_RADIUS)) * 60.0;

    // DDSM uses 0.1 RPM units
    int16_t leftCmd  = (int16_t)(leftRPM * 10.0);
    int16_t rightCmd = (int16_t)(rightRPM * 10.0);

    // Clamp to motor limits
    leftCmd  = constrain(leftCmd, -2100, 2100);
    rightCmd = constrain(rightCmd, -2100, 2100);

    // Send to all four motors
    dc.ddsm_ctrl(LEFT_FRONT,  leftCmd, 2);
    dc.ddsm_ctrl(LEFT_REAR,   leftCmd, 2);

    dc.ddsm_ctrl(RIGHT_FRONT, rightCmd, 2);
    dc.ddsm_ctrl(RIGHT_REAR,  rightCmd, 2);

    // If one side is mounted backwards, uncomment these instead:
    /*
    dc.ddsm_ctrl(RIGHT_FRONT, -rightCmd, 2);
    dc.ddsm_ctrl(RIGHT_REAR,  -rightCmd, 2);
    */
}

void loop()
{
    while (Serial.available())
    {
        char c = Serial.read();

        if (c == '\n')
        {
            float linear = 0.0;
            float angular = 0.0;

            if (sscanf(serialBuffer.c_str(), "%f,%f", &linear, &angular) == 2)
            {
                driveRobot(linear, angular);
            }

            serialBuffer = "";
        }
        else if (c != '\r')
        {
            serialBuffer += c;
        }
    }
}