# volume-blocket
Volume blocklet for i3blocks

Simple, lightweight volume blocklet for i3blocks. One of the issues I ran into with other volume icons were due to using VFIO to run a windows host, I often attached and detached my headphones to/from a virtual machine. This would cause issues with the volume icon updating to the correct audio device. With this, I put the name of the audio device (as shown in the pulseaudio sink info) and it will find the correct pulseaudio sink my headphones are attached to. When there is a change, it pushes a signal (-RTMIN+1) to the i3blocks bar to update it.
