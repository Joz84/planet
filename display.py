def coco():
    params = {
        'image': 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/332937/pluto.jpg',
        'inclinaison': 58.3,
        'rotation_speed': 16.1,
        'size': 300,
        'color': 'rgba(250, 0, 0, 0.4)',
        'shadow': -70,
        'sun_color': 'rgba(250, 212, 0, 0.4)',
        'sun_intensity': 50
    }
        
    root_infos = ['<style>:root {',
        f'--image: url("{params["image"]}");',
        f'--inclinaison: rotate({params["inclinaison"]}deg);',
        f'--rotation-speed: {params["rotation_speed"]};',
        f'--size: {params["size"]}px;',
        f'--color: {params["color"]};',
        f'--shadow: {params["shadow"]}px;',
        f'--sun-color: {params["sun_color"]};',
        f'--sun-intensity: {params["sun_intensity"]}px;'
        '}</style>',
    ]
        
    return ' '.join(root_infos)

print(coco())
    