import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt

# Use mpmath for higher precision in scalar computations.
LD = mp.mpf
PI_LD = LD(mp.pi)


def wrap_angle(angle):
    """
    Wrap an angle to the interval [-pi, pi).

    This keeps directions numerically small, which improves the stability
    of trigonometric functions (sin, cos) when angles are updated many times.
    """
    return (angle + PI_LD) % (2 * PI_LD) - PI_LD


def simulate(a=2.0, D_limit=LD('100.0'), max_steps=10000000000000, digits=80):
    """
    Simulate a stylised hunter - rabbit pursuit in the plane.

    Assumptions of this model (differences compared to the Olympiad problem):
      - In the original problem, both the rabbit and the hunter always move 
        exactly 1 unit per step. In this model, they may move 1 or less
        in each step.


    Interpretation of main variables:
      - A “cycle” is one straight-line movement of both the rabbit and the hunter,
        followed by a change of direction.
      - 'moves' is the distance travelled by the rabbit and the hunter
        during a given cycle.
      - 'D' is the distance between the rabbit and the hunter after each cycle.
      - 'a' is a scaling coefficient determining the value of 'moves' in the next
        cycle based on the current distance 'D': moves = a * D.
      - 'res' is the total accumulated distance travelled.
    """

    mp.mp.dps = digits # Set decimal places for mpmath

    # Initial scalar state: step length, distance, accumulated distance, cycle counter.
    moves = LD(1.0)
    D = LD(0.0)
    res = LD(0.0)
    cycle = 0

    # Initial directions (angles) of rabbit (z) and hunter (m).
    z_angle = LD(0.0)
    m_angle = LD(0.0)

    # Initial positions of rabbit and hunter at the origin.
    z_x = [0.0]
    z_y = [0.0]
    m_x = [0.0]
    m_y = [0.0]

    # Logs for distance, angles and step lengths for later analysis/plotting.
    D_list = [D]
    z_angle_list = [z_angle]
    m_angle_list = [m_angle]
    moves_list = [moves]

    for _ in range(max_steps):
        cycle += 1
        if cycle % 10000 == 0:
            print(f"Cycle {cycle} in high-precision simulation...")

        if cycle == 1:
            # First cycle: start with distance D = 1 and a unit move of the rabbit.
            D = LD(1.0)
            res += LD(1.0)

            # Rabbit moves by 'moves' (currently 1) along its current direction.
            step_z = moves
            new_z_x = z_x[-1] + step_z * mp.cos(z_angle)
            new_z_y = z_y[-1] + step_z * mp.sin(z_angle)

            z_x.append(new_z_x)
            z_y.append(new_z_y)

            # The hunter remains at the starting position in the first cycle because the rabbit has provided him (0;0) coordinates.
            m_x.append(m_x[-1])
            m_y.append(m_y[-1])

            # Update step length for the next cycle according to the parameter 'a'.
            moves = a

            # Rabbit changes direction; the angle change is determined by arcsin(1/moves).
            alfa_new = mp.asin(1.0 / moves)
            z_angle = wrap_angle(z_angle + alfa_new)

            # Store current state after the first cycle.
            D_list.append(D)
            z_angle_list.append(z_angle)
            m_angle_list.append(m_angle)
            moves_list.append(moves)

        else:
            # All subsequent cycles follow an analytic recurrence for the distance D
            #     and for the direction changes of rabbit and hunter.

            # Auxiliary distance term m_dist used in the geometric recurrence.
            m_dist = mp.sqrt(moves * moves - 1.0)

            # Difference along one axis in the chosen coordinate frame.
            x_diff = m_dist - moves + D

            # New distance D between rabbit and hunter at the end of this cycle.
            D = mp.hypot(x_diff, 1.0)

            # Add current step length to the total travelled distance.
            res += moves

            # Store current arcsin(1/moves) for later correction in rabbit's direction.
            alfa_old = mp.asin(1.0 / moves)


            # Move rabbit and hunter straight ahead by moves in their current directions.
            new_z_x = z_x[-1] + moves * mp.cos(z_angle)
            new_z_y = z_y[-1] + moves * mp.sin(z_angle)

            new_m_x = m_x[-1] + moves * mp.cos(m_angle)
            new_m_y = m_y[-1] + moves * mp.sin(m_angle)

            z_x.append(new_z_x)
            z_y.append(new_z_y)
            m_x.append(new_m_x)
            m_y.append(new_m_y)

            # Update hunter's direction based on the current distance D.
            m_angle = wrap_angle(m_angle + mp.asin(1.0 / D))

            # Update step length for the next cycle according to the parameter 'a'.
            moves = a * D

            # Update the rabbit's direction using a combination of the next step length 'np.arcsin(1.0 / moves)', the current distance between the rabbit and the hunter 'np.arcsin(1.0 / D)', the angle value of the rabbit's current direction in the global coordinate system 'z_angle' and the current angle value of the rabbit's movement in the local coordinate system 'alfa_old'.
            z_angle = wrap_angle(
                z_angle
                + mp.asin(1.0 / moves)
                + mp.asin(1.0 / D)
                - alfa_old
            )

            # Log state after this cycle.
            D_list.append(D)
            z_angle_list.append(z_angle)
            m_angle_list.append(m_angle)
            moves_list.append(moves)

        # Stop the simulation once the distance exceeds the given limit.

        if D > D_limit:
            break

    # Return all recorded data in a structured dictionary.
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
    """
    Plot the trajectories of the rabbit and the hunter, and optionally
    display the final distance and number of cycles.
    """
    z_x = [float(x) for x in data["z_x"]]
    z_y = [float(x) for x in data["z_y"]]
    m_x = [float(x) for x in data["m_x"]]
    m_y = [float(x) for x in data["m_y"]]
    D = [float(x) for x in data["D"]]
    cycles = data["cycles"]

    fig, ax = plt.subplots(figsize=(6, 6))

    # Trajectories of rabbit (green) and hunter (red).
    ax.plot(z_x, z_y, color="green", marker='o', linewidth=0.5)
    ax.plot(m_x, m_y, color="red", marker='x', linewidth=0.5)

    # Final segment between rabbit and hunter.
    ax.plot([z_x[-1], m_x[-1]], [z_y[-1], m_y[-1]],
            color="blue", linewidth=0.5)

    if show_D_label:
        # Display distance and number of cycles near the final segment.
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
    a = LD(1.01)
    data = simulate(a=a, D_limit=LD('100.0'))
    print("cycles:", data["cycles"])
    print("final D:", data["D"][-1])
    print("total moves:", data["res"])
    plot_paths(data)



