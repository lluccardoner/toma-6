from controler import GameController


def main():
    controller = GameController(num_players=2, seed=42)
    controller.play()


if __name__ == '__main__':
    main()
