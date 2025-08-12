import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';

export default function AuthForms() {
  return (

      <div className="auth-form-container">
        <div className="auth-form-box">
          <LoginForm />
        </div>
        <div className="auth-form-box">
          <RegisterForm />
        </div>
      </div>

  );
}