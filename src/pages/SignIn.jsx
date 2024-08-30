// LoginPage.js

import { useContext } from 'react';
import AuthContext from '../context/AuthContext';

const SignIn = () => {
    const { loginUser } = useContext(AuthContext);

    const handleSubmit = (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const password = e.target.password.value;
        loginUser(username, password);
        // Redirect to the home page after successful login
        window.location.href = '/';
        // Clear form fields after successful login
        e.target.reset();
        // Display success message
        alert('Login successful');
        // Hide the success message after 3 seconds
        setTimeout(() => {
            alert.close();
        }, 3000);
        // Display error message if login fails
        if (!localStorage.getItem('token')) {
            alert('Invalid credentials');
        }
        // Clear form fields after successful login
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-900 text-gray-100">
            <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-sm">
                <h2 className="text-2xl font-bold mb-6 text-center">Sign In</h2>
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
                        <label htmlFor="password" className="block text-sm font-medium">Password</label>
                        <input 
                            name="password" 
                            type="password" 
                            placeholder="Password" 
                            required 
                            className="mt-1 block w-full px-3 py-2 border border-gray-600 rounded-md bg-gray-700 text-gray-100 focus:outline-none focus:ring focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>
                    <button 
                        type="submit" 
                        className="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        Login
                    </button>
                </form>
            </div>
        </div>
    );
};

export default SignIn;
