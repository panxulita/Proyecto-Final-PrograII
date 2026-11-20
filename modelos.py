from sqlalchemy import String, Integer, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date


class Base(DeclarativeBase):
    pass


class Categoria(Base):

    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descripcion: Mapped[str] = mapped_column(String(250), nullable=False)

    equipos: Mapped[list["Equipo"]] = relationship(back_populates="categoria")

    def __repr__(self):
        return f"Categoria(id={self.id}, nombre={self.nombre}, descripcion={self.descripcion})"


class Equipo(Base):

    __tablename__ = "equipo"

    __table_args__ = (
        CheckConstraint("precio_diario > 0", name="ck_precio_diario"),
        CheckConstraint("stock_total >= 0", name="ck_stock_total"),
        CheckConstraint("stock_disponible >= 0", name="ck_stock_disponible"),
        CheckConstraint("stock_disponible <= stock_total", name="ck_stock_maximo")
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categoria.id"), nullable=False)
    precio_diario: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock_total: Mapped[int] = mapped_column(Integer, nullable=False)
    stock_disponible: Mapped[int] = mapped_column(Integer, nullable=False)

    categoria: Mapped["Categoria"] = relationship(back_populates="equipos")
    arriendos: Mapped[list["Arriendo"]] = relationship(back_populates="equipo")
    
    def __repr__(self):
        return f"Equipo(id={self.id}, nombre={self.nombre}, precio_diario={self.precio_diario}, stock_total={self.stock_total}, stock_disponible={self.stock_disponible})"


class Cliente(Base):

    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)

    arriendos: Mapped[list["Arriendo"]] = relationship(back_populates="cliente")
       
    def __repr__(self):
        return f"Cliente(id={self.id}, nombre={self.nombre}, correo={self.correo}, telefono={self.telefono})"


class Arriendo(Base):

    __tablename__ = "arriendo"

    __table_args__ = (
        CheckConstraint("cantidad > 0", name="ck_cantidad"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    equipo_id: Mapped[int] = mapped_column(ForeignKey("equipo.id"), nullable=False)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"), nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(nullable=False)
    fecha_fin_prevista: Mapped[date] = mapped_column(nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVO")

    equipo: Mapped["Equipo"] = relationship(back_populates="arriendos")
    cliente: Mapped["Cliente"] = relationship(back_populates="arriendos")
