from .shared import Bounds, ImageConfig



def kernel(
        image_config: ImageConfig,
        equation: str,
        max_iter: int,
        bail_mag: float,
        bounds: Bounds
    ) -> str:
    return """
typedef struct {{
    float real;
    float imag;
}} Complex;

Complex squared(Complex z) {{
    Complex result;
    result.real = z.real * z.real - z.imag * z.imag;
    result.imag = 2.0f * z.real * z.imag;
    return result;
}}

Complex add(Complex a, Complex b) {{
    Complex result;
    result.real = a.real + b.real;
    result.imag = a.imag + b.imag;
    return result;
}}

float mag_squared(Complex z) {{
    return z.real * z.real + z.imag * z.imag;
}}


__kernel void render(
    __global float *c_real, __global float *c_imag,
    __global float *z_real, __global float *z_imag,
    __global int *image_data
) 
{{
    int i = get_global_id(0);
    Complex c = {{ c_real[i], c_imag[i] }};
    Complex z = {{ z_real[i], z_imag[i] }};
    Complex locations[{max_iter}];
    int count = 0;

    for (int iter = 0; iter < {max_iter}; iter++) {{
        z = {equation};
        locations[iter] = z;
        count++;
        if (mag_squared(z) > {bail_mag}f) break;
    }}

    if (mag_squared(z) > {bail_mag}f) {{
        for (int j = 0; j < count; j++) {{
            int px = (int)((locations[j].real - {x_min}) / ({x_max} - {x_min}) * {width});
            int py = (int)((locations[j].imag - {y_min}) / ({y_max} - {y_min}) * {height});

            if (px >= 0 && px < {width} && py >= 0 && py < {height}) {{
                atomic_inc(&image_data[py * {width} + px]);
            }}
        }}
    }} else {{
        z_real[i] = z.real;
        z_imag[i] = z.imag;
    }}
}}
""".format(
    equation=equation,
    max_iter=max_iter,
    bail_mag=bail_mag,
    x_min=bounds.x_min,
    x_max=bounds.x_max,
    y_min=bounds.y_min,
    y_max=bounds.y_max,
    width=image_config.width,
    height=image_config.height
)