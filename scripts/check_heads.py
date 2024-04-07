import subprocess


def run_command(cmd):
    try:
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
        )
        # Check if the output has only one line
        output_lines = result.stdout.strip().split("\n")
        if len(output_lines) == 1:
            return output_lines[0]
        else:
            raise Exception("There are more then one migration heads.")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error executing command: {e.stderr}")


command = [
    "poetry",
    "run",
    "alembic",
    "heads",
]  # Replace with your desired shell command
output = run_command(command)
print(output)
