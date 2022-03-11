import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./routes/Home";
import Login from "./routes/Login";
import PasswordReset from "./routes/PasswordReset";
import Signup from "./routes/Signup";
import Market from "./routes/Market";
import StockItemList from "./routes/StockItemList";
import StockItemDetail from "./routes/StockItemDetail";
import BackTestList from "./routes/BackTestList";
import BackTestCreate from "./routes/BackTestCreate";
import BackTestDetail from "./routes/BackTestDetail";
import MyPage from "./routes/MyPage";
import SideBar from "./components/SideBar/SideBar";
import Header from "./components/Header";
import { useEffect, useState } from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Notice from "./routes/Notice";
import NoticeDetail from "./routes/NoticeDetail";

function App() {
  // pathname 을 확인하여, Sidebar 렌더링 여부를 결정
  const [showSideBar, setShowSideBar] = useState(true);
  const noSideBarURL = ["/", "/login", "/signup", "/login/help"];

  useEffect(() => {
    if (noSideBarURL.includes(window.location.pathname)) {
      setShowSideBar(false);
    }
  }, [window.location.pathname]);

  return (
    <Router>
      <ToastContainer hideProgressBar={true} />
      {showSideBar && (
        <div>
          <SideBar />
        </div>
      )}
      <div className={showSideBar ? "ml-20 bg-yellow-50 min-h-screen" : ""}>
        {showSideBar && (
          <div>
            <Header></Header>
          </div>
        )}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/login/help" element={<PasswordReset />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/market" element={<Market />} />
          <Route path="/stock" element={<StockItemList />} />
          <Route path="/stock/:id" element={<StockItemDetail />} />
          <Route path="/backtest" element={<BackTestList />} />
          <Route path="/backtest/create" element={<BackTestCreate />} />
          <Route path="/backtest/:id" element={<BackTestDetail />} />
          <Route path="/mypage" element={<MyPage />} />
          <Route path="/notice" element={<Notice />} />
          <Route path="/notice/:id" element={<NoticeDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;