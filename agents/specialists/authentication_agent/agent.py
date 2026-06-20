# Real DB-based authentication.
# Verifies username, password, role, and user profile.

from db.session import SessionLocal
from db.models import User
from db.employee_repository import verify_password
from shared.logger import logger

class AuthenticationAgent:
    def __init__(self):
        self.agent_name = "AuthenticationAgent"

    def authenticate(self, username: str, password: str) -> dict:
        """
        Authenticate user from database.

        Steps:
        1. Find user by username
        2. Verify hashed password using bcrypt
        3. Check active status
        4. Return user + employee details
        """
        logger.info(f"[{self.agent_name}] Authentication request for user: {username}")

        db = SessionLocal()

        try:
            user = db.query(User).filter_by(username=username).first()

            if not user:
                logger.warning(f"[{self.agent_name}] User not found: {username}")
                return {
                    "agent": self.agent_name,
                    "authenticated": False,
                    "status": "failed",
                    "message": "User not found"
                }

            if not user.is_active:
                logger.warning(f"[{self.agent_name}] Inactive user: {username}")
                return {
                    "agent": self.agent_name,
                    "authenticated": False,
                    "status": "failed",
                    "message": "User account is inactive"
                }

            if not verify_password(password, user.password_hash):
                logger.warning(f"[{self.agent_name}] Invalid password for user: {username}")
                return {
                    "agent": self.agent_name,
                    "authenticated": False,
                    "status": "failed",
                    "message": "Invalid password"
                }

            employee = user.employee

            logger.info(f"[{self.agent_name}] Authentication successful for user: {username}")

            return {
                "agent": self.agent_name,
                "authenticated": True,
                "status": "success",
                "message": "Authentication successful",
                "user": {
                    "user_id": user.id,
                    "employee_db_id": employee.id if employee else None,  # IMPORTANT
                    "username": user.username,
                    "role": user.role,
                    "is_active": user.is_active,
                    "employee_id": employee.employee_id if employee else None,
                    "full_name": employee.full_name if employee else None,
                    "designation": employee.designation if employee else None,
                    "department": employee.department.name if employee and employee.department else None,
                    "email": employee.email if employee else None
                }
            }

        except Exception as e:
            logger.exception(f"[{self.agent_name}] Authentication error for {username}: {str(e)}")
            return {
                "agent": self.agent_name,
                "authenticated": False,
                "status": "error",
                "message": f"Authentication system error: {str(e)}"
            }

        finally:
            db.close()