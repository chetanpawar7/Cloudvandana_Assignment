import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import NoPage from './pages/NoPage';
import Explore from './pages/Explore';
import Navbar from './components/Header/Navbar';
import SignIn from './pages/SignIn';
import SignUp from './pages/Signup';
import './App.css';
import { AuthProvider } from './context/AuthContext';


export default function App() {
  return (
    <>
    <AuthProvider>
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navbar />}>
          <Route index element={<Home />} />
          <Route path="explore" element={<Explore/>} />
          <Route path="about" element={<About/>} />
          <Route path="signin" element={<SignIn/>} />
          <Route path="signup" element={<SignUp/>} />
          <Route path="*" element={<NoPage/>} />
        </Route>
      </Routes>
    </BrowserRouter>
    </AuthProvider>
    </>
  )
}
