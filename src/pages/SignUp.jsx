import { useContext, useState } from 'react';
import AuthContext from '../context/AuthContext';

const SignUp = () => {
    const { registerUser } = useContext(AuthContext);
    const [passwordError, setPasswordError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const email = e.target.email.value;
        const password = e.target.password.value;
        const confirmPassword = e.target.confirmPassword.value;

        if (password !== confirmPassword) {
            setPasswordError("Passwords do not match");
            return;
        } else {
            setPasswordError(''); // Clear any previous error
        }

        await registerUser(username, email, password);

        // Check if registration was successful by checking the authTokens
        if (localStorage.getItem('authTokens')) {
            // Redirect to the home page after successful registration
            window.location.href = '/';
            // Clear form fields after successful registration
            e.target.reset();
            // Display success message
            alert('Registration successful');
        } else {
            // Display error message if registration fails
            alert('Registration failed. Please try again.');
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-900 text-gray-100">
            <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-sm">
                <h2 className="text-2xl font-bold mb-6 text-center">Sign Up</h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label htmlFor="username" className="block text-sm font-medium">Username</label>
                        <input 
                            name="username" 
                            type="text" 
                            placeholder="Username" 
                            required 
                            className="mt-1 block w-full px-3 py-2 border border-gray-600 rounded-md bg-gray-700 text-gray-100 focus:outline-none focus:ring focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>
                    <div>
                        <label htmlFor="email" className="block text-sm font-medium">Email</label>
                        <input 
                            name="email" 
                            type="email" 
                            placeholder="Email" 
                            required 
                            className="mt-1 block w-full px-3 py-2 border border-gray-600 rounded-md bg-gray-700 text-gray-100 focus:outline-none focus:ring focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>
                    <div>
                        <label htmlFor="password" className="block text-sm font-medium">Password</label>
                        <input 
                            name="password" 
                            type="password" 
                            placeholder="Password" 
                            required 
                            className="mt-1 block w-full px-3 py-2 border border-gray-600 rounded-md bg-gray-700 text-gray-100 focus:outline-none focus:ring focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>
                    <div>
                        <label htmlFor="confirmPassword" className="block text-sm font-medium">Confirm Password</label>
                        <input 
                            name="confirmPassword" 
                            type="password" 
                            placeholder="Confirm Password" 
                            required 
                            className="mt-1 block w-full px-3 py-2 border border-gray-600 rounded-md bg-gray-700 text-gray-100 focus:outline-none focus:ring focus:ring-blue-500 focus:border-blue-500"
                        />
                        {passwordError && (
                            <p className="text-red-500 text-sm mt-1">{passwordError}</p>
                        )}
                    </div>
                    <button 
                        type="submit" 
                        className="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        Register
                    </button>
                </form>
            </div>
        </div>
    );
};

export default SignUp;
