from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    COMMON_USER = "common"

    def description(self) -> str:
        descriptions = {
            UserRole.ADMIN: "Administrator with full access privileges.",
            UserRole.COMMON_USER: "Standard user with common access privileges.",
        }
        return descriptions.get(self, f"Description for {self.name} not defined.")