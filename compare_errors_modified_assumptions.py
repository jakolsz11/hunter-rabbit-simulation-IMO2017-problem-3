import matplotlib.pyplot as plt
import numpy as np
import mpmath as mp
from hunter_rabbit_modified_assumptions_float import simulate as simulate_float
from hunter_rabbit_modified_assumptions_hp import simulate as simulate_hp
from config import A


def get_data(a=2.0):
    """
    Get simulation data for both float and high-precision arithmetic.
    """
    print("Starting simulation for float...")
    data_float = simulate_float(a=a, D_limit=100.0)
    print("Float simulation completed.")
    print("Starting simulation for high-precision...")
    data_hp = simulate_hp(a=mp.mpf(str(a)), D_limit=mp.mpf('100.0'))
    print("High-precision simulation completed.")

    return {
        "float": data_float,
        "hp": data_hp,
    }

def compare_data(data):

    n_d = min(len(data["hp"]["D"]), len(data["float"]["D"]))

    if len(data["hp"]["D"]) != len(data["float"]["D"]):
        print(f"Warning: Different lengths of D data: hp={len(data['hp']['D'])}, float={len(data['float']['D'])}")

    result_D = [abs(data["hp"]["D"][i]-data["float"]["D"][i]) for i in range(n_d)]

    n_a = min(len(data["hp"]["z_angle"]), len(data["float"]["z_angle"]))

    if len(data["hp"]["z_angle"]) != len(data["float"]["z_angle"]):
        print(f"Warning: Different lengths of angle data: hp={len(data['hp']['z_angle'])}, float={len(data['float']['z_angle'])}")

    result_angle = [abs(data["hp"]["z_angle"][i]-data["float"]["z_angle"][i]) for i in range(n_a)]
    return{
        "D_difference": result_D,
        "angle_difference": result_angle,
    }


def draw_plots(results):
    D_diff = np.array([float(x) for x in results["D_difference"]])
    angle_diff = np.array([float(x) for x in results["angle_difference"]])

    fig, (ax1_D, ax1_a) = plt.subplots(2, 1, figsize=(12, 8))

    ax1_D.plot(D_diff, color="green", label='Difference in D (linear)', lw=0.7)
    ax1_D.set_xlabel('Cycle')
    ax1_D.set_ylabel('Difference in D (linear)', color="green", fontsize=12)
    ax1_D.grid()
    ax1_D.set_title(f'Difference in Distance D between HP and Float Simulations for a={A}')
    ax1_D.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

    ax2_D = ax1_D.twinx()
    ax2_D.plot(D_diff, color="orange", label='Difference in D (log)', lw=0.7)
    ax2_D.set_ylabel('Difference in D (log)', color="orange", fontsize=12)
    ax2_D.set_yscale('log')
    ax2_D.yaxis.get_offset_text().set_color("orange")
    ax2_D.yaxis.get_offset_text().set_fontsize(10)
    ax2_D.yaxis.get_offset_text().set_position((1.15,0))

    lines1_D, labels1_D = ax1_D.get_legend_handles_labels()
    lines2_D, labels2_D = ax2_D.get_legend_handles_labels()
    ax1_D.legend(lines1_D + lines2_D, labels1_D + labels2_D, loc="lower right")


    ax1_a.plot(angle_diff, color="green", label='Difference in Rabbit Angle (linear)', lw=0.7)
    ax1_a.set_xlabel('Cycle')
    ax1_a.set_ylabel('Difference in Rabbit Angle (linear)', color="green", fontsize=12)
    ax1_a.grid()
    ax1_a.set_title(f'Difference in Rabbit Angle between HP and Float Simulations for a={A}')
    ax1_a.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

    ax2_a = ax1_a.twinx()
    ax2_a.plot(angle_diff, color="orange", label='Difference in Rabbit Angle (log)', lw=0.7)
    ax2_a.set_ylabel('Difference in Rabbit Angle (log)', color="orange", fontsize=12)
    ax2_a.set_yscale('log')

    lines1_a, labels1_a = ax1_a.get_legend_handles_labels()
    lines2_a, labels2_a = ax2_a.get_legend_handles_labels()
    ax1_a.legend(lines1_a + lines2_a, labels1_a + labels2_a, loc="lower right")
    
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.4)
    fig.add_artist(plt.Line2D([0,1], [0.5,0.5], transform=fig.transFigure, color='gray', linestyle='--', linewidth=0.5))
    plt.show()


if __name__ == "__main__":
    data = get_data(a=A)
    results = compare_data(data)
    draw_plots(results)