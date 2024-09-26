#!/usr/bin/env python3

import subprocess
import pulsectl

def get_devices_with_input_and_output():
    with pulsectl.Pulse('set-default-sink') as pulse:
        sinks = pulse.sink_list()
    with pulsectl.Pulse('set-default-source') as pulse:
        sources = pulse.source_list()

    devices_with_input_and_output = []
    for sink in sinks:
        for source in sources:
            if sink.description == source.description:
                devices_with_input_and_output.append((sink, source))

    return devices_with_input_and_output

def switch_default_audio_device(device_index):
    devices = get_devices_with_input_and_output()

    if device_index >= 0 and device_index < len(devices):
        input_device = devices[device_index][1]
        with pulsectl.Pulse('set-default-source') as pulse:
            pulse.source_default_set(input_device)

        output_device = devices[device_index][0]
        with pulsectl.Pulse('set-default-sink') as pulse:
            pulse.sink_default_set(output_device)

def select_device(devices):
    device_list = [f"{device[0].description}" for device in devices]
    rofi_cmd = ['rofi', '-dmenu', '-p', 'Select audio device', '-i', '-format', 'i']
    p = subprocess.Popen(rofi_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
    stdout, _ = p.communicate('\n'.join(device_list))

    if p.returncode == 0:
        try:
            device_index = int(stdout.strip())
            return device_index
        except ValueError:
            pass

    return None

def main():
    devices = get_devices_with_input_and_output()

    if not devices:
        print('No devices found with both audio input and output.')
    else:
        print('Devices with audio input and output:')
        for i, (sink, source) in enumerate(devices):
            print(f'{i + 1}. {sink.description}')

        device_index = select_device(devices)
        # output_device_index = select_device(devices)

        switch_default_audio_device(device_index)
        print('Default audio devices switched successfully.')

if __name__ == '__main__':
    main()