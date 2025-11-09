import Button from "./Button"

export default function Navbar() {
    return (
        <nav className="bg-red-500 flex flex-row top-0 fixed bg-emerald-900">
            <div className="text-lg">
                <a href="/" className="text-sm">ShopAlert</a>
            </div>
            <div>
                <a href="/login">Login</a>
                <Button>Get Started</Button>
            </div>
        </nav>
    )
}