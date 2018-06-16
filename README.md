# petals-lightbox
Guide on creating your own LED installation with Raspberry Pi :>

# How to run
1. Set up your Pi following the guideline on [this library for controlling WS281X LEDs](https://github.com/jgarff/rpi_ws281x), using PWM module
2. Connect the data signal line of your first LED strand with GPIO pin 18 and second with pin 13
3. Adjust brightness, LED count, or any parameter to your custom setup
4. Give bash script permission with "chmod +x script.sh"
5. Run "./script.sh" and you're good to go! :D
