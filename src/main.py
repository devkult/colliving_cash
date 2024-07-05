from domain.entity import Bill, HomeService, User


if __name__ == "__main__":
    home_service = HomeService()

    home = home_service.create_home(name="Home1")

    user1 = home_service.add_user(home=home, name="User1")
    user2 = home_service.add_user(home=home, name="User2")

    home_service.add_bill(
        home=home, user=user1, amount=100, title="Bill1", description="Description1"
    )

    print(home)
