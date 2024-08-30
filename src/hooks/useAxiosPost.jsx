import { useState, useEffect } from 'react';
import axios from 'axios';

const useAxiosPost = (url, postData) => {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('authTokens'); // Retrieve the token from localStorage
        const response = await axios.post(url, postData, {
          headers: {
            'Authorization': `Bearer ${token}`, // Include the token in the request headers
            'Content-Type': 'application/json',
          },
        });
        setData(response.data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url, postData]);

  return { data, error, loading };
};

export default useAxiosPost;
