import mpmath as mp
import matplotlib.pyplot as plt
from config import A, D_LIMIT, MP_PRECISION

"""
This version uses the same geometric and directional logic as the modified-assumptions model, but adapts it to the Olympiad rule that each move must have length exactly 1.
To satisfy this, the continuous step length a·D is replaced by ceil(a·D), meaning the rabbit and hunter always take the maximum possible number of unit steps in each cycle.
All other mechanics (angle updates, recurrence for distance, trajectory rules) remain unchanged.
"""

LD = mp.mpf
PI_LD = LD(mp.pi)


def wrap_angle(angle):
    return (angle + PI_LD) % (2 * PI_LD) - PI_LD


def simulate(a=2.0, D_limit=LD('100.0'), max_steps=10000000000000, digits=80):

    mp.mp.dps = digits

    moves = LD(1.0)
    D = LD(0.0)
    res = LD(0.0)
    cycle = 0

    z_angle = LD(0.0)
    m_angle = LD(0.0)

    z_x = [0.0]
    z_y = [0.0]
    m_x = [0.0]
    m_y = [0.0]

    D_list = [D]
    z_angle_list = [z_angle]
    m_angle_list = [m_angle]
    moves_list = [moves]

    for _ in range(max_steps):
        cycle += 1
        if cycle % 10000 == 0:
            print(f"Cycle {cycle} in high-precision simulation...")

        if cycle == 1:

            D = LD(1.0)
            res += LD(1.0)

            step_z = moves
            new_z_x = z_x[-1] + step_z * mp.cos(z_angle)
            new_z_y = z_y[-1] + step_z * mp.sin(z_angle)

            z_x.append(new_z_x)
            z_y.append(new_z_y)

            m_x.append(m_x[-1])
            m_y.append(m_y[-1])

            moves = mp.ceil(a)

            alfa_new = mp.asin(1.0 / moves)
            z_angle = wrap_angle(z_angle + alfa_new)

            D_list.append(D)
            z_angle_list.append(z_angle)
            m_angle_list.append(m_angle)
            moves_list.append(moves)

        else:
            m_dist = mp.sqrt(moves * moves - 1.0)

            x_diff = m_dist - moves + D

            D = mp.hypot(x_diff, 1.0)

            res += moves

            alfa_old = mp.asin(1.0 / moves)

            new_z_x = z_x[-1] + moves * mp.cos(z_angle)
            new_z_y = z_y[-1] + moves * mp.sin(z_angle)

            new_m_x = m_x[-1] + moves * mp.cos(m_angle)
            new_m_y = m_y[-1] + moves * mp.sin(m_angle)

            z_x.append(new_z_x)
            z_y.append(new_z_y)
            m_x.append(new_m_x)
            m_y.append(new_m_y)

            m_angle = wrap_angle(m_angle + mp.asin(1.0 / D))

            moves = mp.ceil(a * D)

            z_angle = wrap_angle(
                z_angle
                + mp.asin(1.0 / moves)
                + mp.asin(1.0 / D)
                - alfa_old
            )

            D_list.append(D)
            z_angle_list.append(z_angle)
            m_angle_list.append(m_angle)
            moves_list.append(moves)

        if D > D_limit:
            break

    return {
        "z_x": z_x,
        "z_y": z_y,
        "m_x": m_x,
        "m_y": m_y,
        "D": D_list,
        "z_angle": z_angle_list,
        "m_angle": m_angle_list,
        "moves": moves_list,
        "res": res,
        "cycles": cycle,
    }


def plot_paths(data, show_D_label=True):

    z_x = [float(x) for x in data["z_x"]]
    z_y = [float(x) for x in data["z_y"]]
    m_x = [float(x) for x in data["m_x"]]
    m_y = [float(x) for x in data["m_y"]]
    D = [float(x) for x in data["D"]]
    cycles = data["cycles"]

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.plot(z_x, z_y, color="green", marker='o', linewidth=0.5)
    ax.plot(m_x, m_y, color="red", marker='x', linewidth=0.5)

    ax.plot([z_x[-1], m_x[-1]], [z_y[-1], m_y[-1]],
            color="blue", linewidth=0.5)

    if show_D_label:
        mx = 0.5 * (z_x[-1] + m_x[-1])
        my = 0.5 * (z_y[-1] + m_y[-1])
        ax.text(mx, my, f"D={D[-1]:.8f}\nsteps={cycles}",
                color="white", fontsize=8, ha="center")

    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.axis("off")
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")

    plt.show()


if __name__ == "__main__":
    data = simulate(a=LD(A), D_limit=LD(D_LIMIT), digits=MP_PRECISION)
    print("cycles:", data["cycles"])
    print("final D:", data["D"][-1])
    print("total moves:", data["res"])
    plot_paths(data)